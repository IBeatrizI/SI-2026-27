# Fontes e dicionário inicial de dados

## E-REDES — fonte principal

- **Título:** Consumos mensais por concelho
- **URL:** https://e-redes.opendatasoft.com/explore/dataset/3-consumos-faturados-por-municipio-ultimos-10-anos/information/
- **API:** https://e-redes.opendatasoft.com/api/explore/v2.1/catalog/datasets/3-consumos-faturados-por-municipio-ultimos-10-anos/
- **Editora:** E-REDES; **licença:** CC BY 4.0.
- **Histórico declarado:** desde novembro de 2020; ano/mês indica período do consumo, não data da faturação.
- **Grão da fonte:** período mensal × distrito × concelho × freguesia × nível de tensão (confirmar particularidades de agregação RGPD).
- **Atenção:** valores podem ser revistos; alguns consumos são publicados em agregados `OUTROS <Distrito>` por RGPD. Os totais exigem cuidado com a categoria e com a cobertura geográfica.

| Campo API | Tipo documentado | Interpretação |
|---|---|---|
| `ano` | Texto | Ano do consumo; manter como inteiro após validação |
| `mes` | Texto | Mês do consumo (01–12) |
| `mes_int` | Inteiro | Mês numérico |
| `data` | Data | Período mensal |
| `distrito` | Texto | Distrito |
| `concelho` | Texto | Município ou agregado especial |
| `freguesia` | Texto | Freguesia ou agregado especial |
| `nivel_de_tensao` | Texto | Categoria de tensão |
| `energia_ativa_kwh` | Decimal | Consumo faturado em kWh |
| `coddistrito` | Texto | Código do distrito; preservar zeros iniciais |
| `coddistritoconcelho` | Texto | Código territorial para relacionar municípios |
| `coddistritoconcelhofreguesia` | Texto | Código de freguesia |

## DGEG — fonte complementar por recolher

https://www.dgeg.gov.pt/pt/estatistica/energia/eletricidade/consumo-por-municipio-e-setor-de-atividade/

A DGEG disponibiliza consumos **anuais** por município e setor económico (divisões CAE); 2021–2024 estão publicados como **provisórios**. Confirmar ficheiros, formatos, unidades, somas agregadas e eventuais totais que possam duplicar linhas setoriais antes de transformar.

## PORDATA — fonte complementar por recolher

https://www.pordata.pt/municipios/consumo%20de%20energia%20eletrica%20por%20habitante%20total%20e%20por%20tipo%20de%20consumo-435-2048

Indicador municipal anual **kWh/habitante**, com proveniência INE, DGEG/MAE e PORDATA. A página indica atualização em 24/06/2026 e revisão das estimativas de população para 2021–2024. Não multiplicar nem agregar rácios sem considerar os denominadores.

## Registo da descarga (preencher com valores reais)

| Fonte | Ficheiro | Data descarga UTC | URL exportação | SHA256 | Nº registos | Situação |
|---|---|---|---|---|---|---|
| E-REDES | 4 CSV anuais (2021–2024) | 12/11/2026 | Ver manifesto | Ver manifesto | 214 795 | Concluído; [`manifesto versionado`](12_manifesto_recolha_e_redes.json) |
| DGEG | — | — | — | — | — | Por recolher |
| PORDATA | — | — | — | — | — | Por recolher |

## Referências metodológicas

- API Explore v2.1 (exportações sem limite de paginação dos registos): https://help.opendatasoft.com/apis/ods-explore-v2/explore_v2.1.html
- Documentação Microsoft de esquema em estrela: https://learn.microsoft.com/pt-pt/power-bi/guidance/star-schema
