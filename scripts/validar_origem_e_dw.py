#!/usr/bin/env python3
"""Validação INDEPENDENTE: compara os dados brutos com o cubo por mês/distrito/tensão.
Usa só a biblioteca padrão. Não altera os CSVs originais nem as tabelas de factos.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import defaultdict, Counter
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def iter_rows(p, sep=','):
    with p.open('r', encoding='utf-8-sig', newline='') as handle:
        yield from csv.DictReader(handle, delimiter=sep)

def audit(root: Path) -> dict:
    raw=root/'data/raw/e_redes'; proc=root/'data/processed'
    metas=[]; originals=defaultdict(lambda:Decimal('0')); generated=defaultdict(lambda:Decimal('0'))
    counts=Counter(); negative=Counter(); rgpd=Counter(); municipals=defaultdict(set)
    for p in sorted(raw.glob('e_redes_consumos_concelho_*.csv')):
        meta_file=p.with_suffix('.meta.json')
        if not meta_file.exists(): raise ValueError(f'Falta manifesto de origem: {meta_file}')
        meta=json.loads(meta_file.read_text(encoding='utf-8'))
        sha=hashlib.sha256(p.read_bytes()).hexdigest()
        if sha!=meta['sha256']:raise ValueError(f'SHA256 não corresponde à origem: {p.name}')
        size=0
        for r in iter_rows(p,';'):
            size+=1
            ano=int(r['ano']);mes=int(r['mes_int']);dist=r['coddistrito'].zfill(2)
            tensao=r['nivel_de_tensao']
            val=Decimal(r['energia_ativa_kwh'])
            originals[(ano*100+mes,dist,tensao)]+=val
            counts[ano]+=1
            if val<0:negative[ano]+=1
            if 'OUTROS' in r['concelho'].upper():rgpd[ano]+=1
            else:municipals[ano].add(r['coddistritoconcelho'])
        if size!=meta['linhas'] or size!=meta['contagem_api']:
            raise ValueError(f'Contagem do {p.name} não corresponde ao manifesto')
        metas.append({'ano':meta['ano'],'ficheiro':p.name,'sha256':sha,'linhas':size,'recuperado_utc':meta['recuperado_utc']})
    if len(metas)!=4 or set(counts)!=set(range(2021,2025)):
        raise ValueError(f'Faltam ou sobram ficheiros de 2021–2024: {sorted(counts)}')

    locations={r['id_municipio']:r for r in iter_rows(proc/'dim_municipio.csv')}
    tensions={r['id_tensao']:r['nivel_tensao'] for r in iter_rows(proc/'dim_tensao.csv')}
    for r in iter_rows(proc/'fact_consumo_mensal.csv'):
        l=locations.get(r['id_municipio'])
        t=tensions.get(r['id_tensao'])
        if l is None or t is None:raise ValueError('Chave de dimensão órfã nas tabelas processadas')
        p=int(r['id_tempo'])
        generated[(p,l['codigo_distrito'],t)]+=Decimal(r['consumo_kwh'])
    diffs=[]
    for key in sorted(set(originals)|set(generated)):
        a=originals.get(key,Decimal(0));b=generated.get(key,Decimal(0))
        if a!=b:
            diffs.append({'periodo':key[0], 'distrito':key[1], 'tensao':key[2], 'original_kwh':str(a),'processado_kwh':str(b)})
    periods={k[0] for k in originals}
    expected={ano*100+mes for ano in range(2021,2025) for mes in range(1,13)}
    if expected!=periods: raise ValueError(f'Cobertura de meses inválida: {sorted(expected-periods)}')
    if diffs:raise ValueError(f'Reconciliação falhou em {len(diffs)} grupos. Exemplos: {diffs[:5]}')
    report={
        'resultado':'APROVADO','tipo':'reconciliação independente por mês x distrito x tensão',
        'anos':sorted(counts),'meses':len(periods),
        'grupos_reconciliados':len(originals),'grupos_com_diferenca':0,
        'linhas_originais':sum(counts.values()),'linhas_por_ano':dict(sorted(counts.items())),
        'municipios_distintos_por_ano':{str(y):len(s) for y,s in sorted(municipals.items())},
        'consumos_negativos_linhas_por_ano':dict(sorted(negative.items())),
        'linhas_rgpd_por_ano':dict(sorted(rgpd.items())),
        'soma_kwh':str(sum(originals.values(),Decimal(0))),
        'origens':metas,
        'nota':'Verificação da integridade dos ficheiros recolhidos e de igualdade de agregados. Não certifica qualidade estatística nem equivalência com consumo total nacional.'
    }
    path=root/'data/quality/validacao_independente.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"[OK] {report['grupos_reconciliados']} combinações mês/distrito/tensão reconciliadas, sem diferenças")
    print(f"[OK] {report['linhas_originais']} linhas originais, {report['meses']} meses; SHA-256 conferidos")
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--raiz',type=Path,default=ROOT)
    a=ap.parse_args()
    try:audit(a.raiz)
    except Exception as e:ap.exit(1,f'[ERRO] {e}\n')
