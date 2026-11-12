# Resultados exploratórios — E-REDES (2021–2024)

**Natureza:** Resultados calculados de CSVs E-REDES locais. Data registada da recolha: 2026-11-12. Verificar manifestos e hashes; não são resultados inventados ou extrapolados.

**Indicador:** energia ativa faturada (kWh) por mês, localização e nível de tensão; não é sinónimo de toda a energia consumida em Portugal.

## Série anual

| Ano | Energia ativa (TWh) | Variação face ao ano anterior | Parcela geográfica agregada |
|---|---:|---:|---:|
| 2021 | 44.580 | — | 1.2156% |
| 2022 | 45.559 | 2.1948% | 1.2298% |
| 2023 | 45.782 | 0.4904% | 1.2859% |
| 2024 | 46.551 | 1.6789% | 1.2566% |

## Cinco municípios com maior consumo faturado em 2024

| Município | Distrito | GWh (aprox.) |
|---|---|---:|
| Lisboa | Lisboa | 3079.81 |
| Maia | Porto | 1271.20 |
| Porto | Porto | 1245.71 |
| Figueira da Foz | Coimbra | 1206.00 |
| Vila Nova de Gaia | Porto | 1147.44 |

## Controlo de qualidade

- Foram encontrados 48 meses consecutivos e 278 municípios por ano.
- Foram preservadas 185 linhas de consumo negativo e 1111 linhas agregadas como `OUTROS`.
- O relatório `data/quality/validacao_independente.json` verifica os totais por **mês × distrito × nível de tensão**, de forma independente das somas globais do ETL.
- Este conjunto é uma **fotografia da fonte na data de recolha**; os registos podem ser revistos posteriormente no portal.

## Interpretação preliminar

- A série faturada evoluiu de 44.580 TWh em 2021 para 46.551 TWh em 2024 (4.4202% no período).
- Este aumento **não demonstra causalidade**, nem permite concluir sozinho que todos os consumos nacionais cresceram na mesma proporção.
- Os rankings municipais excluem explicitamente membros `OUTROS`/agregados para impedir comparações com municípios fictícios.

## Próximas perguntas a analisar no Power BI

1. Em que meses e anos se observaram os maiores valores?
2. Como muda o ranking quando comparamos valores absolutos por município?
3. Que parte do consumo está associada à baixa tensão?
4. Como varia o consumo entre distritos e dentro de cada distrito?
5. Que diferença aparece entre valores anuais absolutos e kWh por habitante, depois de integrar PORDATA?

## Fontes

- E-REDES: https://e-redes.opendatasoft.com/explore/dataset/3-consumos-faturados-por-municipio-ultimos-10-anos/
- Manifestos de recolha: `data/raw/e_redes/*.meta.json` (ficheiros locais) e `docs/12_manifesto_recolha_e_redes.json` (snapshot original versionado).
- Tabelas geradas: `data/analysis/*.csv` e `data/analysis/indicadores_reais.json`.

**Atenção:** os resultados apresentados aqui foram gerados automaticamente a partir dos dados entregues, não substituindo a discussão e a verificação pelos estudantes.
