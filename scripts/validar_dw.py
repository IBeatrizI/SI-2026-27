#!/usr/bin/env python3
"""Validar chaves, granularidade e soma das tabelas preparadas."""
import argparse
import csv
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def rows(file):
    with file.open(encoding='utf-8-sig', newline='') as f:
        yield from csv.DictReader(f)


def validate(processed:Path, quality:Path):
    fact=list(rows(processed/'fact_consumo_mensal.csv'))
    tempo=list(rows(processed/'dim_tempo.csv'))
    municipio=list(rows(processed/'dim_municipio.csv'))
    tensao=list(rows(processed/'dim_tensao.csv'))
    keys_tempo=[r['id_tempo'] for r in tempo]
    keys_mun=[r['id_municipio'] for r in municipio]
    keys_tens=[r['id_tensao'] for r in tensao]
    errors=[]
    for label,keys in [('tempo',keys_tempo),('municipio',keys_mun),('tensao',keys_tens)]:
        if len(keys)!=len(set(keys)): errors.append(f'Chaves duplicadas em Dim{label}')
        if not keys: errors.append(f'Dim{label} vazia')
    if not fact: errors.append('Tabela de factos vazia')
    seen=set(); total=Decimal('0')
    for r in fact:
        key=(r['id_tempo'],r['id_municipio'],r['id_tensao'])
        if key in seen: errors.append(f'Facto duplicado no grão declarado: {key}')
        seen.add(key)
        if r['id_tempo'] not in keys_tempo: errors.append(f'Tempo sem relação: {key}')
        if r['id_municipio'] not in keys_mun: errors.append(f'Município sem relação: {key}')
        if r['id_tensao'] not in keys_tens: errors.append(f'Tensão sem relação: {key}')
        total+=Decimal(r['consumo_kwh'])
    report=json.loads((quality/'relatorio_etl.json').read_text(encoding='utf-8'))
    expected=Decimal(report['soma_bruta_kwh'])
    if total!=expected: errors.append(f'Totais diferentes: facto={total}; origem={expected}')
    if report['linhas_facto']!=len(fact): errors.append('Contagem de linhas do facto diferente do relatório ETL')
    found=set(r['id_tempo'] for r in tempo)
    for year in report['anos']:
        expected_periods={str(int(year)*100+m) for m in range(1,13)}
        missing=expected_periods-found
        if missing:
            errors.append(f'Aviso: meses em falta em {year}: {sorted(missing)}')
    strong=[e for e in errors if not e.startswith('Aviso:')]
    print('VALIDAÇÃO DW')
    print('DimTempo:',len(tempo),'DimMunicipio:',len(municipio),'DimTensao:',len(tensao),'Factos:',len(fact))
    print('Soma kWh:',total,'| Origem:',expected)
    for problem in errors: print(' -',problem)
    if strong:
        raise ValueError(f'Falharam {len(strong)} validações obrigatórias')
    print('[OK] Chaves, granularidade e soma de energia verificadas')
    return {'dim_tempo':len(tempo),'dim_municipio':len(municipio),'dim_tensao':len(tensao),'factos':len(fact),'consumo_kwh':str(total),'avisos':[e for e in errors if e.startswith('Aviso:')]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--processados',type=Path,default=ROOT/'data'/'processed')
    parser.add_argument('--qualidade',type=Path,default=ROOT/'data'/'quality')
    args=parser.parse_args()
    try: validate(args.processados,args.qualidade)
    except (OSError,ValueError,KeyError) as exc: parser.exit(1,f'ERRO: {exc}\n')

if __name__=='__main__': main()
