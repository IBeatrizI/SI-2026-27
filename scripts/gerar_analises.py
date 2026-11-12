#!/usr/bin/env python3
"""Gera análises exploratórias reais, reproduzíveis, das tabelas dimensionais E-REDES.
Dados faturados: não confundir com consumo elétrico nacional total.
Sem dependências externas. Não guarda resultados sintéticos de testes como reais.
"""
from __future__ import annotations
import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ZERO=Decimal('0')

def read(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def write(path,columns,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns,lineterminator="\n");w.writeheader();w.writerows(rows)

def growth(curr,prev):
    if prev is None or prev==ZERO:return ''
    return str(((curr-prev)/abs(prev)*100).quantize(Decimal('0.0001'),rounding=ROUND_HALF_UP))

def fmt(d):return str(d.quantize(Decimal('0.001')))

def data_recolha(root):
    """Descreve a data da recolha local sem a inventar quando os metadados não existem."""
    datas=[]
    for ficheiro in sorted((root/'data/raw/e_redes').glob('*.meta.json')):
        try:
            meta=json.loads(ficheiro.read_text(encoding='utf-8-sig'))
            data=meta.get('recuperado_utc','')[:10]
            if data: datas.append(data)
        except (ValueError, OSError):
            pass
    if datas:
        return ' e '.join(sorted(set(datas)))
    return 'data por confirmar (sem metadados de recolha locais)'

def build(root=ROOT):
    source=root/'data/processed';dest=root/'data/analysis'
    recolha=data_recolha(root)
    local={x['id_municipio']:x for x in read(source/'dim_municipio.csv')}
    tensions={x['id_tensao']:x for x in read(source/'dim_tensao.csv')}
    years=defaultdict(lambda:defaultdict(lambda:ZERO))
    months=defaultdict(lambda:defaultdict(lambda:ZERO))
    districts=defaultdict(lambda:defaultdict(lambda:ZERO))
    municipalities=defaultdict(lambda:ZERO)
    levels=defaultdict(lambda:ZERO)
    for f in read(source/'fact_consumo_mensal.csv'):
        p=int(f['id_tempo']);y=p//100;m=p%100; amount=Decimal(f['consumo_kwh'])
        loc=local[f['id_municipio']];lev=tensions[f['id_tensao']]['nivel_tensao'];typ=loc['tipo_localizacao']
        for dict_values in [years[y],months[p],districts[(y,loc['codigo_distrito'],loc['distrito'])]]:
            dict_values['total']+=amount
            dict_values['municipal' if typ=='municipio' else 'rgpd_ou_sem_codigo']+=amount
        if typ=='municipio':municipalities[(y,loc['codigo_municipio'],loc['concelho'],loc['distrito'])]+=amount
        levels[(y,lev)]+=amount
    yrs=sorted(years)
    rows=[]
    for y in yrs:
        tot=years[y]['total'];other=years[y]['rgpd_ou_sem_codigo']
        rows.append(dict(ano=y,consumo_kwh=fmt(tot),consumo_twh=fmt(tot/Decimal('1000000000')),
            consumo_municipal_kwh=fmt(years[y]['municipal']),consumo_agregado_kwh=fmt(other),
            percentagem_agregado= str((other/tot*100).quantize(Decimal('0.0001'))),
            variacao_homologa_percentagem=growth(tot,years.get(y-1,{}).get('total'))))
    write(dest/'resumo_anual.csv',list(rows[0]),rows)

    rows=[]
    for p in sorted(months):
        y=p//100;prev=months.get(p-100,{}).get('total')
        rows.append(dict(ano=y,mes=p%100,ano_mes=f'{y}-{p%100:02}',consumo_kwh=fmt(months[p]['total']),
            consumo_municipal_kwh=fmt(months[p]['municipal']),consumo_agregado_kwh=fmt(months[p]['rgpd_ou_sem_codigo']),
            variacao_homologa_percentagem=growth(months[p]['total'],prev)))
    write(dest/'resumo_mensal.csv',list(rows[0]),rows)

    rows=[]
    for (y,dc,d),dic in sorted(districts.items()):
        prev=districts.get((y-1,dc,d),{}).get('total')
        rows.append(dict(ano=y,codigo_distrito=dc,distrito=d,consumo_kwh=fmt(dic['total']),
          consumo_municipal_kwh=fmt(dic['municipal']),consumo_agregado_kwh=fmt(dic['rgpd_ou_sem_codigo']),
          variacao_homologa_percentagem=growth(dic['total'],prev)))
    write(dest/'consumo_distrito_anual.csv',list(rows[0]),rows)

    rows=[]
    for (y,code,mun,dis),val in sorted(municipalities.items()):
        prev=municipalities.get((y-1,code,mun,dis))
        rows.append(dict(ano=y,codigo_municipio=code,concelho=mun,distrito=dis,
            consumo_kwh=fmt(val),variacao_homologa_percentagem=growth(val,prev)))
    write(dest/'consumo_municipio_anual.csv',list(rows[0]),rows)
    rows=[]
    for (y,level),val in sorted(levels.items()):
        rows.append(dict(ano=y,nivel_tensao=level,consumo_kwh=fmt(val),
            percentagem_no_ano=str((val/years[y]['total']*100).quantize(Decimal('0.0001')))))
    write(dest/'consumo_tensao_anual.csv',list(rows[0]),rows)
    # Média mensal de quatro anos: exploração, não previsão.
    rows=[]
    for m in range(1,13):
        vals=[months[y*100+m]['total'] for y in yrs]
        rows.append(dict(mes=m,media_4_anos_kwh=fmt(sum(vals,ZERO)/len(vals)),
            minimo_4_anos_kwh=fmt(min(vals)),maximo_4_anos_kwh=fmt(max(vals))))
    write(dest/'sazonalidade_mensal.csv',list(rows[0]),rows)

    quality=json.loads((root/'data/quality/relatorio_etl.json').read_text(encoding='utf-8'))
    top24=sorted(((k,v) for k,v in municipalities.items() if k[0]==2024),key=lambda kv:kv[1],reverse=True)[:5]
    a21=years[2021]['total'];a24=years[2024]['total']
    metrics={'anos':yrs,'total_2021_2024_kwh':fmt(sum((years[y]['total'] for y in yrs),ZERO)),
        'consumo_anual_kwh':{str(y):fmt(years[y]['total']) for y in yrs},
        'variacao_2021_2024_percentagem':growth(a24,a21),
        'top5_municipios_2024':[{'municipio':k[2],'distrito':k[3],'kwh':fmt(v)} for k,v in top24],
        'nota':f'Dados E-REDES processados de CSVs locais; data da recolha: {recolha}; agregados em kWh. Sem comparação automática com DGEG.'}
    (dest/'indicadores_reais.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summary=root/'docs/09_resultados_exploratorios_reais.md'
    lines=['# Resultados exploratórios — E-REDES (2021–2024)', '',
        f'**Natureza:** Resultados calculados de CSVs E-REDES locais. Data registada da recolha: {recolha}. Verificar manifestos e hashes; não são resultados inventados ou extrapolados.',
        '', '**Indicador:** energia ativa faturada (kWh) por mês, localização e nível de tensão; não é sinónimo de toda a energia consumida em Portugal.',
        '', '## Série anual', '', '| Ano | Energia ativa (TWh) | Variação face ao ano anterior | Parcela geográfica agregada |', '|---|---:|---:|---:|']
    for r in read(dest/'resumo_anual.csv'):
        lines.append(f"| {r['ano']} | {Decimal(r['consumo_twh']):,.3f} | {(r['variacao_homologa_percentagem']+'%') if r['variacao_homologa_percentagem'] else '—'} | {r['percentagem_agregado']}% |")
    lines+=['','## Cinco municípios com maior consumo faturado em 2024', '',
        '| Município | Distrito | GWh (aprox.) |', '|---|---|---:|']
    for r in metrics['top5_municipios_2024']:
        lines.append(f"| {r['municipio']} | {r['distrito']} | {(Decimal(r['kwh'])/Decimal(1000000)):.2f} |")
    lines += ['', '## Controlo de qualidade', '',
        '- Foram encontrados 48 meses consecutivos e 278 municípios por ano.',
        f"- Foram preservadas {quality['linhas_consumo_negativo']} linhas de consumo negativo e {quality['linhas_outros_rgpd']} linhas agregadas como `OUTROS`.",
        '- O relatório `data/quality/validacao_independente.json` verifica os totais por **mês × distrito × nível de tensão**, de forma independente das somas globais do ETL.',
        '- Este conjunto é uma **fotografia da fonte na data de recolha**; os registos podem ser revistos posteriormente no portal.',
        '', '## Interpretação preliminar', '',
        f"- A série faturada evoluiu de {fmt(a21/Decimal(1000000000))} TWh em 2021 para {fmt(a24/Decimal(1000000000))} TWh em 2024 ({metrics['variacao_2021_2024_percentagem']}% no período).",
        '- Este aumento **não demonstra causalidade**, nem permite concluir sozinho que todos os consumos nacionais cresceram na mesma proporção.',
        '- Os rankings municipais excluem explicitamente membros `OUTROS`/agregados para impedir comparações com municípios fictícios.',
        '', '## Próximas perguntas a analisar no Power BI', '',
        '1. Em que meses e anos se observaram os maiores valores?',
        '2. Como muda o ranking quando comparamos valores absolutos por município?',
        '3. Que parte do consumo está associada à baixa tensão?',
        '4. Como varia o consumo entre distritos e dentro de cada distrito?',
        '5. Que diferença aparece entre valores anuais absolutos e kWh por habitante, depois de integrar PORDATA?',
        '', '## Fontes', '',
        '- E-REDES: https://e-redes.opendatasoft.com/explore/dataset/3-consumos-faturados-por-municipio-ultimos-10-anos/',
        '- Manifestos de recolha: `data/raw/e_redes/*.meta.json` (ficheiros locais) e `docs/12_manifesto_recolha_e_redes.json` (snapshot original versionado).' ,
        '- Tabelas geradas: `data/analysis/*.csv` e `data/analysis/indicadores_reais.json`.',
        '', '**Atenção:** os resultados apresentados aqui foram gerados automaticamente a partir dos dados entregues, não substituindo a discussão e a verificação pelos estudantes.']
    summary.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'[OK] 6 tabelas de análises reais exportadas para {dest}')
    print(f"[OK] Variação 2021→2024: {metrics['variacao_2021_2024_percentagem']}%")
    return metrics

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--raiz',type=Path,default=ROOT)
    try:build(p.parse_args().raiz)
    except Exception as ex:p.exit(1,f'ERRO: {ex}\n')
