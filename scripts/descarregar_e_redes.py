#!/usr/bin/env python3
"""Descarregar CSVs reais por ano da E-REDES e verificar a contagem de registos.

Utiliza apenas a biblioteca padrão de Python; exige acesso à Internet na máquina
que executa o script. Não gera dados artificiais e não substitui ficheiros
existentes sem --substituir. Fonte: E-REDES OpenData / Explore API v2.1.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATASET = '3-consumos-faturados-por-municipio-ultimos-10-anos'
API_BASE = f'https://e-redes.opendatasoft.com/api/explore/v2.1/catalog/datasets/{DATASET}'
FIELDS = {'ano', 'mes', 'data', 'distrito', 'concelho', 'freguesia',
          'nivel_de_tensao', 'energia_ativa_kwh', 'coddistrito',
          'coddistritoconcelho', 'coddistritoconcelhofreguesia', 'mes_int'}
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'data' / 'raw' / 'e_redes'


def request_bytes(url: str, *, max_tries: int = 3) -> bytes:
    last_exc = None
    for attempt in range(max_tries):
        try:
            request = urllib.request.Request(url, headers={
                'User-Agent': 'SI-Energia-Data-Study/1.0 (academic research)',
                'Accept': 'application/json, text/csv, */*',
            })
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_exc = exc
            if attempt < max_tries - 1:
                time.sleep(min(2 ** attempt + 1, 8))
    raise RuntimeError(f'Falha na ligação à API após {max_tries} tentativas: {last_exc}')


def api_url(suffix: str, **params: str) -> str:
    return f'{API_BASE}/{suffix}?{urllib.parse.urlencode(params)}'


def expected_count(ano: int) -> tuple[int, str]:
    url = api_url('records', where=f"ano = '{ano}'", limit='1')
    content = request_bytes(url)
    info = json.loads(content.decode('utf-8-sig'))
    count = info.get('total_count')
    if not isinstance(count, int) or count <= 0:
        raise ValueError(f'API não forneceu uma contagem válida para {ano}: {info!r}')
    return count, url


def verify_csv(path: Path, ano: int) -> tuple[int, str]:
    with path.open('r', encoding='utf-8-sig', newline='') as handle:
        sample = handle.read(4096)
        handle.seek(0)
        if sample.lstrip().startswith(('{', '<', '[')):
            raise ValueError('Resposta não parece ser um CSV; pode ser HTML/JSON de erro')
        first_line = sample.splitlines()[0] if sample else ''
        separator = ';' if first_line.count(';') >= first_line.count(',') else ','
        reader = csv.DictReader(handle, delimiter=separator)
        header = set(reader.fieldnames or [])
        missing = FIELDS - header
        if missing:
            raise ValueError(f'Colunas esperadas em falta: {sorted(missing)}')
        total = 0
        for line in reader:
            total += 1
            if str(line.get('ano', '')).strip() != str(ano):
                raise ValueError(f'Ano inesperado na linha {total}: {line.get("ano")!r}')
        if not total:
            raise ValueError('CSV vazio')
        return total, separator


def download_year(ano: int, dest: Path, *, substituir: bool) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / f'e_redes_consumos_concelho_{ano}.csv'
    manifest = dest / f'e_redes_consumos_concelho_{ano}.meta.json'
    if target.exists() and not substituir:
        count, _ = verify_csv(target, ano)
        print(f'[EXISTENTE] {ano}: {count:,} linhas. Usar --substituir para atualizar.')
        return {'ano': ano, 'linhas': count, 'ficheiro': str(target), 'estado': 'existente'}

    count_api, query_url = expected_count(ano)
    export_url = api_url('exports/csv', where=f"ano = '{ano}'",
                         delimiter=';', with_bom='false')
    data = request_bytes(export_url)
    tmp = dest / f'.{target.name}.tmp'
    try:
        tmp.write_bytes(data)
        count_csv, delimiter = verify_csv(tmp, ano)
        if count_csv != count_api:
            raise ValueError(
                f'Exportação incompleta ou fonte alterada: CSV={count_csv}, API={count_api} '
                '(não se substituiu o original). Repetir depois de verificar o portal.')
        digest = hashlib.sha256(data).hexdigest()
        meta = {
            'fonte': 'E-REDES Open Data',
            'dataset': DATASET,
            'licenca': 'CC BY 4.0',
            'ano': ano,
            'recuperado_utc': datetime.now(timezone.utc).isoformat(),
            'url_exportacao': export_url,
            'url_contagem': query_url,
            'linhas': count_csv,
            'contagem_api': count_api,
            'sha256': digest,
            'delimitador': delimiter,
            'nota': 'Exportação completa para o ano segundo a contagem da API no momento da descarga.',
        }
        os.replace(tmp, target)
        manifest.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'[OK] {ano}: {count_csv:,} linhas, SHA256 {digest[:14]}…, {target}')
        return meta
    finally:
        if tmp.exists():
            tmp.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description='Descarregar e verificar CSVs E-REDES por ano')
    parser.add_argument('--anos', nargs='+', type=int, default=[2021, 2022, 2023, 2024])
    parser.add_argument('--destino', type=Path, default=DEST)
    parser.add_argument('--substituir', action='store_true', help='Recarregar ficheiros já existentes')
    args = parser.parse_args()
    try:
        for ano in args.anos:
            if not 2020 <= ano <= 2100:
                raise ValueError(f'Ano fora do intervalo esperado: {ano}')
            download_year(ano, args.destino, substituir=args.substituir)
    except (RuntimeError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f'ERRO: {exc}')
        return 1
    print('Dados descarregados e verificados. Próximo: python scripts/perfil_e_redes.py')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
