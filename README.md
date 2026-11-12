# SI · Análise multidimensional do consumo de energia elétrica em Portugal

**Sistemas de Informação (SI)** · Trabalho Prático n.º 1 · **2026/2027**

Licenciatura em Engenharia Informática · **Projeto de grupo**

> **Estado — Fase 2 (12/11/2026):** recolha e ETL da **E-REDES (2021–2024) executados com dados reais**; validações aprovadas; modelo em estrela e resultados exploratórios em CSV. **Ainda não há dashboard Power BI/PBIX concluído, integração DGEG/PORDATA, vídeo ou relatório final.**

[**Guia rápido**](docs/GUIA_EXECUCAO.md) · [**Resultados exploratórios**](docs/09_resultados_exploratorios_reais.md) · [**Modelo dimensional**](model/modelo_estrela.md) · [**Power BI/OLAP**](docs/10_powerbi_olap_fase2.md) · [**Publicar no GitHub**](docs/08_partilha_github.md) · [**Alterações desta versão**](CHANGELOG.md)

## 1. Objetivo e perguntas de análise

O projeto pretende aplicar **ETL, modelação multidimensional, Business Intelligence e operações OLAP** a dados públicos de **energia elétrica faturada** em Portugal continental. A análise inicial cobre **janeiro de 2021 a dezembro de 2024**.

Perguntas principais:

1. Como evoluiu a energia elétrica faturada, por mês e por ano?
2. Que diferenças existem entre distritos e municípios?
3. Que padrões sazonais se observam?
4. Qual é a distribuição por nível de tensão?
5. Como varia o consumo por **setor de atividade**? *(fase futura: DGEG)*
6. Como comparar municípios pelo indicador de **kWh por habitante**? *(fase futura: PORDATA)*

**Limite de interpretação:** os totais da E-REDES referem-se à cobertura e à metodologia de energia ativa **faturada** deste dataset; não representam automaticamente todo o consumo energético de Portugal nem devem ser somados a indicadores DGEG/PORDATA sem harmonização.

## 2. Fontes de dados

| Fonte e dataset | Granularidade / medida | Estado |
|---|---|---|
| [E-REDES — Consumos mensais por concelho](https://e-redes.opendatasoft.com/explore/dataset/3-consumos-faturados-por-municipio-ultimos-10-anos/information/) | Mês × localização × nível de tensão; kWh de energia ativa faturada | **Recolhido, tratado e validado** para 2021–2024 |
| [DGEG — Consumo por município e setor](https://www.dgeg.gov.pt/pt/estatistica/energia/eletricidade/consumo-por-municipio-e-setor-de-atividade/) | Município × setor × ano; unidades por confirmar no ficheiro | **Por recolher e integrar** |
| [PORDATA — Consumo de eletricidade por habitante](https://www.pordata.pt/municipios/consumo+de+energia+eletrica+por+habitante+total+e+por+tipo+de+consumo-435) | Município × indicador × ano; kWh/habitante | **Por recolher e integrar** |

A recolha E-REDES foi efetuada em **12/11/2026**. A fonte pode corrigir ou rever séries históricas. Os **anos, contagens, URLs de exportação e SHA-256** da recolha original estão no [manifesto versionado](docs/12_manifesto_recolha_e_redes.json). Atribuição: **E-REDES Open Data — CC BY 4.0**.

> Importante: PORDATA pode reutilizar estatísticas produzidas pela DGEG/INE. Portais diferentes não garantem independência estatística; a origem de cada indicador deve ser identificada.

## 3. Fase 2: o que está efetivamente concluído

| Componente | Evidência no projeto | Estado |
|---|---|---|
| Recolha dos 4 CSV E-REDES | Manifesto SHA-256 e contagens API | Concluído (snapshot 12/11/2026) |
| ETL e validação | Scripts Python e `data/quality/` | Concluído para E-REDES |
| Modelo multidimensional inicial | `model/`, CSVs gerados e consultas `.pq` | Preparado; **ainda não importado/validado no Power BI** |
| Resultados exploratórios | `data/analysis/` e `docs/09_*` | Gerados com os dados reais |
| Integração DGEG/PORDATA | Plano em `docs/11_*` | Pendente |
| Dashboards e demonstração OLAP | Guias e medidas DAX propostas | Pendente de implementação/teste |
| Relatório, vídeo e declaração de IA | Orientações em `docs/05_*` | Pendente |

**Resultados da recolha e validação:**

| Indicador | Resultado |
|---|---:|
| Registos originais E-REDES | **214 795** |
| Períodos mensais | **48** |
| Municípios identificados | **278** |
| Membros territoriais especiais (RGPD) | **18** |
| Registos do facto mensal após agregação | **27 702** |
| Grupos reconciliados (mês × distrito × tensão) | **1 728** |
| Grupos com diferenças | **0** |

O relatório preserva **185 observações com consumo negativo** e **1 111 linhas territoriais `OUTROS`** da fonte. Os totais anuais e os resultados geográficos estão detalhados em [`docs/09_resultados_exploratorios_reais.md`](docs/09_resultados_exploratorios_reais.md).

## 4. Metodologia e modelo multidimensional

```text
E-REDES Open Data (API/CSV)
            │
            ▼
Extração por ano + controlo de linhas e SHA-256
            │
            ▼
Perfil dos dados → limpeza/normalização → agregação (ETL)
            │
            ▼
  DimTempo ──────────┐
  DimMunicipio ──────┼── FactConsumoMensal (kWh)
  DimTensao ─────────┘
            │
            ▼
Validação de chaves e reconciliação independente
            │
            ▼
Power BI (por construir): medidas, visuais e OLAP
```

O grão da tabela de factos é **mês × membro territorial × nível de tensão**. Cada dimensão liga-se à tabela de factos por uma relação **1:N**, com filtragem da dimensão para o facto. Os membros `OUTROS` são mantidos como agregados de distrito, **não** como municípios fictícios. Valores negativos não são removidos sem justificação.

Os dados anuais da DGEG e da PORDATA, quando validados, deverão usar **factos separados**, sem replicar um valor anual por todos os meses. **kWh/habitante não é uma medida aditiva.** Ver o [modelo em estrela](model/modelo_estrela.md) e o [plano multifonte](docs/11_integracao_dgeg_pordata.md).

## 5. Estrutura do repositório

```text
README.md                      Visão geral, âmbito e estado
INICIAR_WINDOWS.bat            Testes + download + ETL + validações + análises
CONTINUAR_WINDOWS.bat          Reprocessar dados já descarregados (sem Internet)
docs/README.md                 Índice da documentação
docs/GUIA_EXECUCAO.md          Instalação e execução no Windows
docs/08_partilha_github.md     Fluxo de branches, commit e Pull Request
docs/12_manifesto_recolha_e_redes.json  Proveniência verificada dos CSV originais
scripts/                       Descarregamento, ETL, perfil, validações, análise
tests/                         Testes automáticos com dados SINTÉTICOS
model/                         Esquema dimensional e SQL opcional
powerbi/                       Consultas Power Query, DAX e guia de visuais
data/analysis/                 CSVs e indicadores exploratórios versionados
data/quality/                  Relatórios JSON de validação versionados
data/raw/                      CSVs brutos locais (excluídos do Git)
data/processed/                Ficheiros de dimensões/factos gerados (excluídos do Git)
```

No GitHub estão disponíveis **scripts, documentação e resultados exploratórios leves**. Os CSV brutos e as tabelas processadas ficam fora do Git e podem ser **reconstruídos com o script de recolha**. Para trabalhar sem Internet, utilizar o arquivo local completo, distribuído separadamente pelo grupo.

## 6. Execução no Windows

**Requisitos:** Python **3.10+**, com `py` configurado; ligação à Internet para uma nova descarga. Scripts sem dependências Python externas. Power BI Desktop é necessário **apenas para a fase de BI**.

Na raiz do repositório, em PowerShell:

```powershell
py --version
py -m unittest discover -s tests -v
```

**Primeira execução (recolher, tratar e validar):**

```powershell
.\INICIAR_WINDOWS.bat
```

**Se os CSV originais já estiverem em `data/raw/e_redes/` (sem descarregar novamente):**

```powershell
.\CONTINUAR_WINDOWS.bat
```

Ambos os scripts param quando um passo falha. O [guia de execução](docs/GUIA_EXECUCAO.md) inclui os comandos Python equivalentes e explica como verificar os resultados. O relatório de qualidade não substitui a revisão humana dos indicadores.

## 7. Power BI e próximas fases

1. **Construir um novo PBIX** importando os quatro CSVs de `data/processed/` com as consultas em `powerbi/consultas/`.
2. Validar as **três relações 1:N**, tipos e medidas DAX, comparando totais com `data/quality/relatorio_etl.json`.
3. Construir páginas temporal, geográfica e por nível de tensão; demonstrar *Roll-up, Drill-down, Slice, Dice* e *Pivot* com dados reais.
4. Caracterizar e integrar **DGEG/PORDATA**, respeitando grãos anuais, unidades e proveniência.
5. Elaborar **relatório técnico**, **vídeo(s)** e a **Declaração de Uso de IA** exigidos no enunciado.

Guias: [Power BI](powerbi/GUIA_POWER_BI.md) · [Plano OLAP](docs/10_powerbi_olap_fase2.md) · [DGEG/PORDATA](docs/11_integracao_dgeg_pordata.md).


**Fonte:** [E-REDES Open Data](https://e-redes.opendatasoft.com/) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). **Snapshot:** 12/11/2026. Nenhum dashboard, execução Power BI ou integração multifonte é declarado como concluído antes da respetiva validação.
