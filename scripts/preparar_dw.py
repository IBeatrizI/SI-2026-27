#!/usr/bin/env python3
"""Transformar CSVs originais E-REDES em esquema em estrela (fase inicial).

A execução nunca cria valores sintéticos. Registos 'OUTROS' são preservados
num membro agregado por distrito, sem atribuição a município real.
A soma da medida no facto deve ser exatamente igual à soma dos registos fonte.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw' / 'e_redes'
OUT = ROOT / 'data' / 'processed'
QUALITY = ROOT / 'data' / 'quality'
REQUIRED = {'ano', 'mes', 'data', 'distrito', 'concelho',
            'nivel_de_tensao', 'energia_ativa_kwh', 'coddistrito',
            'coddistritoconcelho', 'mes_int'}
MONTHS = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho',
          'Agosto','Setembro','Outubro','Novembro','Dezembro']


def parse_decimal(raw: str) -> Decimal:
    value = (raw or '').strip().replace('\u00a0', '').replace(' ', '')
    if not value:
        raise ValueError('consumo em branco')
    # A API normalmente usa ponto decimal. Quando só há vírgula, permite vírgula decimal.
    if ',' in value and '.' in value:
        raise ValueError(f'formato numérico ambíguo (ponto e vírgula): {raw!r}')
    if value.count(',') > 1 or value.count('.') > 1:
        raise ValueError(f'formato numérico inválido: {raw!r}')
    try:
        num = Decimal(value.replace(',', '.'))
    except InvalidOperation as exc:
        raise ValueError(f'consumo não numérico: {raw!r}') from exc
    if not num.is_finite():
        raise ValueError(f'consumo não finito: {raw!r}')
    return num


def read_csv(path: Path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        first = f.readline()
        delimiter = ';' if first.count(';') >= first.count(',') else ','
        f.seek(0)
        r = csv.DictReader(f, delimiter=delimiter)
        missing = REQUIRED - set(r.fieldnames or [])
        if missing:
            raise ValueError(f'{path.name}: colunas em falta {sorted(missing)}')
        for number, row in enumerate(r, 2):
            yield number, row


def key_slug(s: str) -> str:
    text = ''.join(ch for ch in unicodedata.normalize('NFKD', s) if not unicodedata.combining(ch))
    text = re.sub(r'[^A-Za-z0-9]+', '_', text.upper()).strip('_')
    return text or 'SEM_DESCRICAO'


def norm_code(raw: str, width: int) -> str:
    s = (raw or '').strip()
    return s.zfill(width) if s.isdigit() and len(s) <= width else ''


def build(paths: list[Path], output: Path = OUT, quality_dir: Path = QUALITY) -> dict:
    if not paths:
        raise ValueError('Não foram indicados CSVs de origem')
    facts = defaultdict(lambda: Decimal('0'))
    locations = {}
    tensions = {}
    years = Counter()
    months = Counter()
    n_rows = 0
    raw_total = Decimal('0')
    negative_rows = 0
    outros_rows = 0
    missing_codes = 0
    name_conflicts = set()
    errors = []
    unique_years = set()
    names_seen = {}
    source_digests = {}

    for file in paths:
        if not file.is_file():
            raise FileNotFoundError(f'Ficheiro original em falta: {file}')
        source_digests[file.name] = hashlib.sha256(file.read_bytes()).hexdigest()
        filename_year = re.search(r'_(20\d\d)\.csv$', file.name)
        for line_no, row in read_csv(file):
            n_rows += 1
            try:
                ano = int((row.get('ano') or '').strip())
                mes_source = (row.get('mes_int') or row.get('mes') or '').strip()
                mes = int(mes_source)
                if not (2020 <= ano <= 2100 and 1 <= mes <= 12):
                    raise ValueError('ano/mês fora do intervalo')
                mes_alt = (row.get('mes') or '').strip()
                if mes_alt and mes_alt.isdigit() and int(mes_alt) != mes:
                    raise ValueError('mes e mes_int são inconsistentes')
                data = (row.get('data') or '').strip()
                if data and not data.startswith(f'{ano:04d}-{mes:02d}'):
                    raise ValueError(f'data inconsistente: {data}')
                if filename_year and int(filename_year.group(1)) != ano:
                    raise ValueError('ano não corresponde ao nome do ficheiro')
                nome_distrito = (row.get('distrito') or '').strip()
                nome_concelho = (row.get('concelho') or '').strip()
                codigo_distrito = norm_code(row.get('coddistrito'), 2)
                codigo_concelho = norm_code(row.get('coddistritoconcelho'), 4)
                tensao = (row.get('nivel_de_tensao') or '').strip()
                if not nome_distrito or not tensao:
                    raise ValueError('distrito ou nível de tensão vazio')
                consumo = parse_decimal(row.get('energia_ativa_kwh'))
                if consumo < 0:
                    negative_rows += 1
                freguesia = (row.get('freguesia') or '').strip()
                is_outros = any('OUTROS' in s.upper() for s in (nome_concelho, freguesia))
                if is_outros:
                    outros_rows += 1
                    loc_type = 'agregado_rgpd'
                    loc_key = f'OUTROS_{codigo_distrito or key_slug(nome_distrito)}'
                    loc_name = f'OUTROS — {nome_distrito}'
                    loc_code = ''
                elif codigo_concelho:
                    loc_type = 'municipio'
                    loc_key = codigo_concelho
                    loc_name = nome_concelho or f'Município {codigo_concelho} (sem nome)'
                    loc_code = codigo_concelho
                else:
                    missing_codes += 1
                    loc_type = 'sem_codigo'
                    loc_key = f'SEMCOD_{codigo_distrito or key_slug(nome_distrito)}_{key_slug(nome_concelho)}'
                    loc_name = nome_concelho or 'Sem município identificável'
                    loc_code = ''
                loc_new = (loc_key, loc_code, loc_name, codigo_distrito, nome_distrito, loc_type)
                if loc_key in locations:
                    old = locations[loc_key]
                    if old[3:] != loc_new[3:] or (loc_type == 'municipio' and old[2] != loc_new[2]):
                        name_conflicts.add((loc_key, old[2], loc_new[2]))
                        # Conserva o primeiro nome e avisa; não inventa equivalências.
                else:
                    locations[loc_key] = loc_new
                t_key = key_slug(tensao)
                if t_key in tensions and tensions[t_key] != tensao:
                    raise ValueError(f'Colisão de chave entre níveis de tensão: {tensions[t_key]!r}/{tensao!r}')
                tensions[t_key] = tensao
                period = ano * 100 + mes
                facts[(period, loc_key, t_key)] += consumo
                raw_total += consumo
                years[ano] += 1
                months[period] += 1
                unique_years.add(ano)
            except (ValueError, TypeError) as exc:
                errors.append(f'{file.name}: linha {line_no}: {exc}')
                if len(errors) >= 30:
                    break
        if errors:
            break

    if errors:
        raise ValueError('Existem erros na origem; nenhuma tabela de saída foi escrita:\n' + '\n'.join(errors))
    if not n_rows:
        raise ValueError('Nenhum registo recebido')
    result_total = sum(facts.values(), Decimal('0'))
    if result_total != raw_total:
        raise ValueError(f'Falha de reconciliação: {raw_total} != {result_total}')

    output.mkdir(parents=True, exist_ok=True)
    quality_dir.mkdir(parents=True, exist_ok=True)

    def write_csv(filename: str, header: list[str], rows):
        target = output / filename
        with target.open('w', encoding='utf-8-sig', newline='') as handle:
            writer = csv.writer(handle, delimiter=',', lineterminator='\n')
            writer.writerow(header)
            writer.writerows(rows)
        return str(target)

    periods = sorted(months)
    write_csv('dim_tempo.csv', ['id_tempo','ano','mes','trimestre','semestre','nome_mes','ano_mes'],
              [(p, p//100, p%100, (p%100-1)//3+1, (p%100-1)//6+1,
                MONTHS[p%100-1], f'{p//100:04d}-{p%100:02d}') for p in periods])
    write_csv('dim_municipio.csv',
              ['id_municipio','codigo_municipio','concelho','codigo_distrito','distrito','tipo_localizacao'],
              [locations[k] for k in sorted(locations)])
    write_csv('dim_tensao.csv', ['id_tensao','nivel_tensao'],
              [(k, tensions[k]) for k in sorted(tensions)])
    write_csv('fact_consumo_mensal.csv',
              ['id_tempo','id_municipio','id_tensao','consumo_kwh'],
              [(p, m, t, str(facts[(p,m,t)])) for p,m,t in sorted(facts)])

    report = {
        'data_processamento_utc': datetime.now(timezone.utc).isoformat(),
        'estado': 'ETL executado sobre ficheiros locais; verificar relatório e integridade antes de interpretar resultados',
        'ficheiros_origem_sha256': source_digests,
        'linhas_fonte': n_rows,
        'linhas_facto': len(facts),
        'periodos': periods,
        'meses_presentes': len(periods),
        'anos': dict(sorted(years.items())),
        'linhas_por_mes': {str(k): v for k,v in sorted(months.items())},
        'dim_municipio_total': len(locations),
        'dim_tensao_total': len(tensions),
        'linhas_outros_rgpd': outros_rows,
        'linhas_sem_codigo_municipio': missing_codes,
        'linhas_consumo_negativo': negative_rows,
        'conflitos_nomes_localizacao': [list(x) for x in sorted(name_conflicts)],
        'soma_bruta_kwh': str(raw_total),
        'soma_factos_kwh': str(result_total),
        'diferenca_kwh': str(raw_total - result_total),
        'notas': [
            'Os dados são faturados no período de consumo, conforme metadados E-REDES.',
            'Valores negativos não foram eliminados automaticamente.',
            'OUTROS RGPD permanece em membros territoriais agregados por distrito, não em município real.',
            'Registos sem código válido são retidos e marcados; investigar antes de juntar a DGEG/PORDATA.',
            'Não interpretar resultados sem verificar cobertura e compatibilidade das fontes.'
        ],
    }
    (quality_dir / 'relatorio_etl.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description='Preparar tabelas dimensionais da E-REDES')
    parser.add_argument('--origem', type=Path, default=RAW)
    parser.add_argument('--saida', type=Path, default=OUT)
    parser.add_argument('--qualidade', type=Path, default=QUALITY)
    args = parser.parse_args()
    paths = sorted(args.origem.glob('e_redes_consumos_concelho_*.csv'))
    if not paths:
        parser.error('Não existem CSVs originais. Executa primeiro scripts/descarregar_e_redes.py')
    try:
        result = build(paths, args.saida, args.qualidade)
    except (ValueError, OSError, FileNotFoundError) as exc:
        parser.exit(1, f'ERRO: {exc}\n')
    print(f"[OK] {result['linhas_fonte']} linhas fonte → {result['linhas_facto']} linhas de factos")
    print(f"[OK] Soma kWh: {result['soma_bruta_kwh']} | diferença: {result['diferenca_kwh']}")
    print(f"[INFO] OUTROS RGPD: {result['linhas_outros_rgpd']} linhas")
    print(f"[INFO] Meses observados: {result['meses_presentes']}")
    print(f"[INFO] Verificações: {args.qualidade / 'relatorio_etl.json'}")


if __name__ == '__main__':
    main()
