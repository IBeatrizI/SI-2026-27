# Estado e limitações verificadas — 12/11/2026

**Já confirmado com dados reais:** 4 CSV originais E-REDES, 214 795 linhas, 48 meses, 278 municípios e 18 membros RGPD, 27 702 linhas de factos. Ver `data/quality/relatorio_etl.json` e `data/quality/validacao_independente.json`.

**Validação:** integridade SHA256 dos ficheiros, contagens da API registadas na recolha, reconciliados os consumos por mês/distrito/tensão em 1 728 grupos, sem diferenças.

**Limitações:** trata-se de energia ativa faturada na rede/cobertura E-REDES, não de todo o consumo energético nacional. A E-REDES pode rever valores históricos; os ficheiros são uma fotografia de 12/11/2026. Os registos `OUTROS` mantêm-se agregados e não entram em rankings municipais. Consumidores/setores/per capita não podem ser inferidos apenas desta fonte.

**Por fazer:** ETL DGEG/PORDATA, Power BI configurado, visuais BI/OLAP, análise integrada, relatório e vídeo de apresentação.

**Publicação GitHub:** os relatórios de qualidade e os resultados exploratórios leves estão versionados. Os CSV brutos e as dimensões/factos processados ficam fora do Git; reproduzir pelo script. O [manifesto publicado](12_manifesto_recolha_e_redes.json) conserva a proveniência original.
