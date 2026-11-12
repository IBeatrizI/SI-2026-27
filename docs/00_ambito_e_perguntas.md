# Fase 1 — âmbito, problema e perguntas

## Âmbito definido para a Fase 2 (a rever se necessário)

- **Tema:** consumo de energia elétrica em Portugal.
- **Período inicial:** 2021–2024. Seleção conservadora para compatibilidade com DGEG e PORDATA; não indica que todas as fontes tenham cobertura completa.
- **Âmbito:** Portugal continental, inicialmente analisado pelos distritos e municípios cobertos pela E-REDES.
- **Medida principal:** energia ativa faturada (kWh), **não produção nem energia consumida efetiva medida em tempo real**.
- **Ferramenta prevista:** Power BI Desktop + Power Query + medidas DAX; scripts Python opcionais para extração/ETL reproduzível.

## Objetivo

Integrar e analisar dados de consumo elétrico com diferentes granularidades temporais e espaciais para identificar padrões e construir indicadores comparativos, demonstrando processos ETL, modelação multidimensional e operações OLAP.

## Questões de análise e dados necessários

| ID | Questão | Dados necessários | Análise esperada |
|---|---|---|---|
| Q1 | Como variou o consumo mensal/anual em 2021–2024? | E-REDES, ano/mês/kWh | Gráfico de linhas e roll-up mês→ano |
| Q2 | Quais as diferenças entre distritos e municípios? | E-REDES, geografia/kWh | Matriz + drill-down distrito→município |
| Q3 | Que padrões sazonais existem? | E-REDES, mês/ano/kWh | Comparação de meses e anos |
| Q4 | Qual o peso de cada nível de tensão? | E-REDES, tensão/kWh | Colunas empilhadas e filtros |
| Q5 | Quais os setores com maior consumo anual? | DGEG, município/setor/ano | Análise setorial anual **a implementar** |
| Q6 | Qual é o consumo anual por habitante? | PORDATA, município/ano/kWh por habitante | Comparação relativa anual **a implementar** |

**Cautela:** As medidas de DGEG e PORDATA podem sobrepor-se estatisticamente à E-REDES e entre si. Não somar indiscriminadamente métricas distintas ou dividir medidas sem compatibilização.

## Critérios de aceitação da fase

- [x] Dados E-REDES descarregados com data/hash. DGEG/PORDATA pendentes.
- [x] Confirmada a cobertura mensal E-REDES 2021–2024 (48 meses).
- [x] Identificados 18 membros territoriais `OUTROS` (RGPD).
- [x] Registadas contagens e alertas no relatório ETL E-REDES.
- [x] Reconciliação E-REDES fonte → factos igual a zero; 1 728 grupos aprovados.
- [ ] Modelo dimensional e relações discutidos pelo grupo.
- [ ] DGEG e PORDATA caracterizadas antes de integrar.
