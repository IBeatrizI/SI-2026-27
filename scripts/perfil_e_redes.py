#!/usr/bin/env python3
"""Auditoria exploratória dos CSVs originais E-REDES, sem os alterar."""
import argparse
import json
from collections import Counter
from pathlib import Path
from preparar_dw import RAW, read_csv, parse_decimal


def main():
    parser = argparse.ArgumentParser(description='Diagnóstico de qualidade dos CSV E-REDES')
    parser.add_argument('--origem', type=Path, default=RAW)
    args = parser.parse_args()
    files = sorted(args.origem.glob('e_redes_consumos_concelho_*.csv'))
    if not files:
        parser.error('Sem CSVs originais. Executa primeiro descarregar_e_redes.py')
    errors=[]; years=Counter(); months=Counter(); tensoes=Counter(); blank=Counter()
    negative=0; outros=0; total=0; par_concelhos=set()
    for file in files:
        for lineno, row in read_csv(file):
            total+=1
            for col,v in row.items():
                if v is None or not str(v).strip(): blank[col]+=1
            years[str(row.get('ano',''))]+=1
            months[(str(row.get('ano','')),str(row.get('mes_int','')))]+=1
            tensoes[str(row.get('nivel_de_tensao',''))]+=1
            par_concelhos.add((str(row.get('coddistritoconcelho','')), str(row.get('concelho',''))))
            if any('OUTROS' in str(row.get(k,'')).upper() for k in ['concelho','freguesia']): outros+=1
            try:
                if parse_decimal(row.get('energia_ativa_kwh')) < 0: negative+=1
            except ValueError as exc:
                if len(errors)<20: errors.append(f'{file.name}:{lineno}: {exc}')
    result={
        'ficheiros':[str(x) for x in files],
        'linhas':total,
        'anos':dict(years),
        'periodos': {f'{a}-{m}':n for (a,m),n in sorted(months.items())},
        'niveis_tensao':dict(tensoes),
        'combinacoes_codigo_nome_concelho':len(par_concelhos),
        'nulos_por_coluna':dict(blank),
        'linhas_consumo_negativo':negative,
        'linhas_outros_rgpd':outros,
        'erros_energia_encontrados':errors,
        'nota':'Diagnóstico sem limpeza. O total de municípios deve ser validado com código de município e RGPD.'
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__=='__main__': main()
