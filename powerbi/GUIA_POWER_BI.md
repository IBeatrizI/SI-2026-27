# Power BI Desktop — criar um PBIX novo

**Pré-requisito:** os quatro CSVs já existem em `data/processed/`, criados pelo ETL com dados reais e validados por `py scripts/validar_dw.py`.

## 1. Criar um PBIX novo e um parâmetro

1. Abrir **Power BI Desktop → Ficheiro → Novo**.
2. Selecionar **Transformar dados → Gerir parâmetros → Novo parâmetro**.
3. Criar um parâmetro **Texto** com nome `pDataFolder` e valor absoluto, por exemplo:
   `C:\Projetos\si-energia-bi-2026-2027\data\processed`
4. Verificar se a pasta existe no disco. Não colocar o nome de um ficheiro no valor do parâmetro.

## 2. Importar as quatro tabelas

Em **Transformar dados → Nova origem → Consulta em branco → Editor Avançado**, copiar o conteúdo dos ficheiros da pasta `powerbi/consultas/` para cada consulta com o nome exato:

- `DimTempo.pq` → `DimTempo`
- `DimMunicipio.pq` → `DimMunicipio`
- `DimTensao.pq` → `DimTensao`
- `FactConsumoMensal.pq` → `FactConsumoMensal`

As colunas de texto preservam zeros iniciais. Os valores decimais do ficheiro processado utilizam ponto decimal; o código M força a interpretação `en-US` para impedir diferenças de localização regional.

## 3. Relações (vista Modelo)

Criar **três** relações ativas de filtragem em direção única (1 → *):

- `DimTempo[id_tempo]` (1) → `FactConsumoMensal[id_tempo]` (*)
- `DimMunicipio[id_municipio]` (1) → `FactConsumoMensal[id_municipio]` (*)
- `DimTensao[id_tensao]` (1) → `FactConsumoMensal[id_tensao]` (*)

Garantir que o Power BI não cria relações automáticas incorretas. Não criar relações diretas entre factos (na futura integração DGEG/PORDATA).

## 4. Criar medidas e hierarquias

Copiar as medidas de `MEDIDAS_DAX.md` para uma tabela de medidas ou para `FactConsumoMensal`.

Criar hierarquia `Distrito → Concelho` na `DimMunicipio`; criar hierarquia `Ano → Mês` em `DimTempo`. Ordenar `DimTempo[nome_mes]` por `DimTempo[mes]` quando necessário. Não marcar uma dimensão com apenas um registo por mês como calendário diário completo.

## 5. Primeiros visuais e operações OLAP

- **Linha temporal:** `ano_mes` no eixo e medida consumo kWh no valor.
- **Matriz territorial:** hierarquia Distrito → Concelho e consumo kWh no valor. Para ranking estritamente municipal, filtrar `tipo_localizacao = municipio`.
- **Barras por tensão:** `nivel_tensao` e consumo kWh.
- **Segmentadores:** ano, distrito e nível de tensão.
- Demonstrar **Roll-up**, **Drill-down**, **Slice**, **Dice** e **Pivot** em análise ou vídeo com dados reais.

## 6. Validar no Power BI

- A medida `Consumo (kWh)` sem filtros deve reconciliar com `soma_factos_kwh` do ficheiro `data/quality/relatorio_etl.json`.
- A soma de consumos por tensão deve reconciliar com a medida total.
- A soma por distrito pode incluir `OUTROS` quando não existem filtros de localização; mostrar a distinção nas conclusões.
- A variância YoY deve ser vazia no primeiro ano se não existirem meses equivalentes no ano anterior.

**Este pacote não inclui um `.pbix` executado ou screenshots de resultados. Para um plano detalhado do dashboard com métricas reais, consultar `docs/10_powerbi_olap_fase2.md`.** Esses ficheiros têm de ser produzidos pelos estudantes após a importação real.
