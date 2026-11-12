# Plano de análise BI e operações OLAP

A componente de **análise BI e OLAP corresponde a 40% da avaliação**; a aplicação deve ser demonstrada num vídeo do Power BI com filtros, hierarquias e resultados obtidos com dados reais.

## Modelo inicial

DimTempo (mês e ano), DimMunicipio (distrito e município/agregado), DimTensao, FactConsumoMensal (kWh). Filtrar `tipo_localizacao = municipio` nos rankings de municípios. Para totais por distrito, indicar claramente se o agregado RGPD está incluído.

## Páginas recomendadas

| Página | Visualizações | Demonstração |
|---|---|---|
| 1. Visão geral | Total kWh, evolução mensal e por ano | **Slice** por ano; indicador total |
| 2. Temporal | Linhas mensais, matriz ano × mês | **Roll-up** de mês para ano |
| 3. Geográfica | Barras por distrito e matriz hierárquica | **Drill-down** distrito → concelho |
| 4. Tensão | Barras empilhadas por nível | **Dice** por ano, distrito e tensão |
| 5. Setorial *(futura)* | Consumo por setor e ano (DGEG) | **Pivot** e comparação anual |
| 6. Per capita *(futura)* | kWh/hab. por município (PORDATA) | Filtros anuais e comparação |

## Operações OLAP

- **Roll-up:** navegar mês → ano (soma da mesma medida aditiva).
- **Drill-down:** distrito → município em hierarquia real do visual.
- **Slice:** fixar 2024 para comparar municípios nesse ano.
- **Dice:** filtrar em simultâneo 2022–2024, distrito e nível de tensão.
- **Pivot:** trocar linhas e colunas numa matriz dinâmica (ex.: anos e distritos).

## Validações

- Todas as medidas expressam unidades claras.
- A agregação de kWh usa **soma**; rácios como kWh/habitante não devem ser somados.
- Medidas por município excluem, quando apropriado, registos `OUTROS`.
- Verificar que filtros e relações não duplicam valores.
- Não apresentar comparação `produção vs consumo` como se fossem dados do mesmo indicador.
