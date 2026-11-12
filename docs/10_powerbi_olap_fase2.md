# Fase 2 — Power BI e primeiras análises OLAP

> **Ponto de situação:** a E-REDES 2021–2024 está recolhida, transformada e validada em CSV. Este documento serve para criar **um novo ficheiro PBIX no Power BI Desktop**. Não existe, nesta entrega, um PBIX criado automaticamente ou um vídeo demonstrativo.

## 1. Importar o modelo em estrela

1. Abrir **Power BI Desktop** → **Novo** e guardar como `powerbi/SI_Energia_Consumo.pbix`.
2. **Transformar dados** → **Gerir parâmetros** → novo parâmetro Texto `pDataFolder` com o caminho absoluto da pasta `data\processed`.
3. Para cada consulta em `powerbi/consultas/`, criar **Nova consulta → Consulta em branco → Editor Avançado**, colar o código e dar-lhe o nome indicado:
   - `DimTempo.pq` → `DimTempo`;
   - `DimMunicipio.pq` → `DimMunicipio`;
   - `DimTensao.pq` → `DimTensao`;
   - `FactConsumoMensal.pq` → `FactConsumoMensal`.
4. Em **Fechar e aplicar**, confirmar que são importadas 48 linhas de `DimTempo`, 296 linhas de `DimMunicipio` (**278 municípios + 18 membros agregados RGPD**), 2 linhas de `DimTensao` e 27 702 factos. São as contagens do *snapshot* incluído neste ZIP, que podem mudar se os dados da E-REDES forem descarregados novamente.
5. Em **Vista Modelo**, configurar relações ativas, **1:* / filtro único**, da dimensão para o facto:
   - `DimTempo[id_tempo]` → `FactConsumoMensal[id_tempo]`;
   - `DimMunicipio[id_municipio]` → `FactConsumoMensal[id_municipio]`;
   - `DimTensao[id_tensao]` → `FactConsumoMensal[id_tensao]`.
6. Verificar os tipos de dados: IDs de localização e tensão como **Texto**; `consumo_kwh` como **Número decimal**; `id_tempo` como **Número inteiro**.
7. Criar a hierarquia `Distrito > Concelho` na `DimMunicipio`; para uma hierarquia temporal, usar `Ano > Mês`. Ordenar `nome_mes` por `mes`. A dimensão contém meses, **não é uma tabela de datas diárias**.

## 2. Medidas DAX (adicionar no menu Modelação → Nova medida)

As medidas de base já estão em `powerbi/MEDIDAS_DAX.md`. Acrescentar estas medidas:

```dax
Consumo (TWh) =
DIVIDE([Consumo (kWh)], 1000000000)
```

```dax
Peso Geografia Agregada (%) =
DIVIDE(
    CALCULATE(
        [Consumo (kWh)],
        DimMunicipio[tipo_localizacao] <> "municipio"
    ),
    [Consumo (kWh)]
)
```

```dax
Número de Municípios =
CALCULATE(
    DISTINCTCOUNT(DimMunicipio[codigo_municipio]),
    DimMunicipio[tipo_localizacao] = "municipio",
    NOT ISBLANK(DimMunicipio[codigo_municipio])
)
```

Formatar as medidas percentuais como `%` (a função DAX devolve uma fração, não multiplicar por 100).

## 3. Dashboard proposto: 3 páginas nesta fase

### Página A — Visão Geral
- Cartões: `Consumo (TWh)`, `Consumo Municipal (kWh)`, `Peso Geografia Agregada (%)`.
- Gráfico de linhas: `DimTempo[ano_mes]` no eixo e `Consumo (kWh)` como valor.
- Gráfico de colunas: `DimTempo[ano]` e `Consumo (TWh)`.
- Segmentadores: `ano` e `nivel_tensao`.
- Validar os cartões anuais com `data/analysis/resumo_anual.csv`.

### Página B — Comparação geográfica
- Matriz com `DimMunicipio[distrito] > [concelho]` nas linhas, `DimTempo[ano]` nas colunas e `Consumo (kWh)` como valores.
- Barras dos 15 municípios com maior consumo; filtro visual obrigatório `DimMunicipio[tipo_localizacao] = municipio`.
- Segmentadores de ano e nível de tensão.
- **Drill-down:** distrito → município; **Pivot:** alternar ano entre linhas e colunas; **Dice:** selecionar vários anos e distritos.
- Valores de referência por município: `data/analysis/consumo_municipio_anual.csv`.

### Página C — Níveis de tensão e sazonalidade
- Gráfico de barras por `DimTensao[nivel_tensao]` com `Consumo (kWh)`.
- Matriz com ano nas linhas e mês nas colunas (consumo) e filtros por distrito.
- **Slice:** selecionar um ano; **Roll-up:** de mês para ano; **Dice:** combinar distrito, período e tensão.
- Validar totais com `data/analysis/consumo_tensao_anual.csv` e `resumo_mensal.csv`.

## 4. Critérios de aceitação antes de gravar o vídeo

- O cartão sem filtros deve apresentar **182 472 494 439,000 kWh**, a soma dos anos de 2021–2024 no snapshot do projeto.
- Os totais anuais e por tensão devem bater certo com os CSVs em `data/analysis`.
- Nenhuma linha `OUTROS` deve aparecer num ranking de **municípios reais**.
- Fazer uma seleção de ano e nível de tensão e demonstrar que os valores filtram corretamente.
- A medida `Consumo Ano Anterior (kWh)` deve ficar vazia em 2021, pois não existe 2020 neste modelo.
- Usar nos títulos **“Energia ativa faturada — E-REDES”** ou equivalente, e não “Consumo total nacional”.

## 5. Evidência de avaliação

Gravar **capturas reais** do Power BI após importar, criar relações e construir os visuais. O vídeo deve mostrar interações efetivas de *Roll-up, Drill-down, Slice, Dice e Pivot*. Não gerar screenshots ilustrativas como se fossem resultados executados.

**Próximo objetivo:** importar DGEG e PORDATA como factos anuais independentes, conforme `docs/11_integracao_dgeg_pordata.md`.
