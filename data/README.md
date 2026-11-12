# Dados e resultados

| Pasta | Conteúdo | Versionamento |
|---|---|---|
| `raw/e_redes/` | CSVs originais da E-REDES e metadados por ano | **Não incluídos no Git**; reobtidos pela API |
| `raw/dgeg/` | Ficheiros originais DGEG, ainda pendentes | **Não incluídos no Git** |
| `raw/pordata/` | Ficheiros originais PORDATA, ainda pendentes | **Não incluídos no Git** |
| `processed/` | Dimensões e factos após ETL | **Não incluídos no Git**; reconstruídos pelos scripts |
| `quality/` | Relatórios JSON do snapshot verificado | **Incluídos no Git** |
| `analysis/` | CSVs analíticos e indicadores do snapshot verificado | **Incluídos no Git** |

Os resultados em `analysis/` e `quality/` correspondem à recolha da E-REDES de **12/11/2026**. A origem e os hashes dos CSVs brutos podem ser verificados em [`../docs/12_manifesto_recolha_e_redes.json`](../docs/12_manifesto_recolha_e_redes.json).

A ausência dos CSVs brutos no GitHub **não significa que o ETL foi executado no computador de quem clona o repositório**. Para os obter e reconstruir as tabelas, executar `INICIAR_WINDOWS.bat`. Quando já estão presentes localmente, usar `CONTINUAR_WINDOWS.bat`.

Não editar manualmente os CSVs de origem nem alterar resultados calculados para os fazer coincidir com um valor esperado. Uma nova versão da fonte pode produzir métricas diferentes.
