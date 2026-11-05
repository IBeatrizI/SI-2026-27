# Análise Multidimensional do Consumo de Energia Elétrica em Portugal

**Sistemas de Informação | Trabalho Prático n.º 1 | 2026/2027**

Projeto académico desenvolvido no âmbito da unidade curricular de **Sistemas de Informação**, da Licenciatura em Engenharia Informática da Universidade Politécnica de Beja.

O trabalho tem como tema **Energia** e pretende explorar a utilização de técnicas de *Business Intelligence* (BI), processos ETL (*Extract, Transform, Load*), modelação multidimensional (*Data Warehouse*) e análise OLAP para estudar dados reais do setor energético português.

## 1. Enquadramento

O setor energético produz grandes quantidades de informação sobre consumos, distribuição e utilização de eletricidade.

Através da integração e análise de dados provenientes de diferentes fontes, é possível identificar padrões de consumo, acompanhar a evolução temporal dos indicadores energéticos e comparar diferentes regiões geográficas.

Neste contexto, o projeto pretende transformar dados públicos sobre o consumo de energia elétrica em informação estruturada e relevante para análise e apoio à decisão.

## 2. Objetivos do projeto

### Objetivo geral

Desenvolver uma solução de Business Intelligence que permita integrar, organizar e analisar dados relativos ao consumo de energia elétrica em Portugal, recorrendo a um modelo multidimensional e a técnicas de análise OLAP.

### Objetivos específicos

- Recolher dados energéticos reais de diferentes fontes públicas.
- Identificar e avaliar a qualidade dos datasets selecionados.
- Desenvolver um processo ETL para integrar e transformar os dados.
- Definir um modelo multidimensional adequado às necessidades de análise.
- Organizar os dados para suportar consultas analíticas.
- Aplicar técnicas de Business Intelligence e operações OLAP.
- Construir visualizações, gráficos e tabelas dinâmicas.
- Identificar tendências, padrões e diferenças no consumo energético.
- Documentar o processo e apresentar os resultados obtidos.

## 3. Âmbito do estudo

A proposta inicial consiste em analisar o consumo de energia elétrica nos municípios de Portugal continental, considerando a evolução ao longo do tempo e as diferenças entre regiões.

| Elemento | Definição inicial |
|---|---|
| Tema | Energia |
| Área de estudo | Consumo de energia elétrica |
| Abrangência | Portugal continental |
| Período de análise | 2021–2024 (provisório) |
| Fonte principal | E-REDES |
| Fonte complementar | PORDATA |
| Indicador principal | Consumo de energia elétrica (kWh) |
| Indicador complementar | Consumo por habitante (kWh/hab.) |
| Tipo de análise | Temporal, geográfica e multidimensional |

**Nota:** O período, os indicadores e o âmbito geográfico poderão ser ajustados após a exploração e validação dos datasets.

## 4. Questões de análise

O desenvolvimento do projeto será orientado por um conjunto de questões:

1. Como evoluiu o consumo de energia elétrica em Portugal ao longo dos anos?
2. Quais são os municípios que apresentam maiores e menores consumos?
3. Existem padrões sazonais no consumo de eletricidade?
4. Como se distribui o consumo pelos diferentes níveis de tensão?
5. Que diferenças existem entre municípios em termos de consumo por habitante?

Estas questões permitirão orientar a seleção dos dados, a definição do modelo multidimensional e a construção das análises.

## 5. Fontes de dados

### 5.1. E-REDES — Fonte principal

**Portal:** https://e-redes.opendatasoft.com/pages/homepage/

A E-REDES disponibiliza dados abertos sobre a rede de distribuição de eletricidade em Portugal.

Pretende-se utilizar o dataset de consumos mensais por concelho, que contém informação sobre o consumo de eletricidade ao longo do tempo, por localização geográfica e nível de tensão.

**Informação relevante:**
- Ano e mês;
- Distrito e concelho;
- Freguesia, quando aplicável;
- Nível de tensão;
- Energia ativa consumida (kWh).

### 5.2. PORDATA — Fonte complementar

**Portal:** https://www.pordata.pt/

A PORDATA disponibiliza indicadores estatísticos que poderão complementar os dados energéticos da E-REDES.

Pretende-se explorar indicadores relacionados com o consumo de energia elétrica por habitante.

A integração será realizada apenas após verificar a compatibilidade temporal, geográfica e metodológica entre as fontes.

### 5.3. Outras fontes

Poderão ser consideradas outras fontes, como o IPMA, caso contribuam para responder às questões definidas e acrescentem valor à análise.

## 6. Metodologia de desenvolvimento

O projeto encontra-se organizado em seis fases.

### Fase 1 — Definição e exploração dos dados

**Objetivo:** estabelecer o âmbito do estudo e identificar os dados necessários.

Atividades:
- Analisar o enunciado do trabalho;
- Definir o problema e os objetivos;
- Formular as questões de análise;
- Identificar as fontes de dados;
- Explorar os datasets disponíveis;
- Verificar períodos temporais, formatos e campos;
- Avaliar a compatibilidade entre as fontes.

**Resultado esperado:** proposta de estudo definida e datasets identificados e caracterizados.

### Fase 2 — Preparação e integração dos dados (ETL)

**Objetivo:** transformar os dados recolhidos numa estrutura coerente e adequada para análise.

O processo ETL será organizado em três etapas:

**Extract — Extração**
- Obter os datasets das fontes selecionadas;
- Preservar os ficheiros originais;
- Registar a origem e a data de recolha.

**Transform — Transformação**
- Identificar valores nulos e duplicados;
- Uniformizar formatos de datas e unidades;
- Normalizar identificadores geográficos;
- Tratar inconsistências;
- Definir as regras de agregação;
- Preparar os dados para integração.

**Load — Carregamento**
- Carregar os dados transformados no modelo de armazenamento escolhido;
- Validar a integridade e consistência dos resultados.

**Resultado esperado:** dados tratados, integrados e documentados.

### Fase 3 — Modelação multidimensional

**Objetivo:** definir um modelo Data Warehouse adequado às análises pretendidas.

Atividades:
- Definir a granularidade dos dados;
- Identificar factos e medidas;
- Identificar dimensões e hierarquias;
- Definir as relações entre as tabelas;
- Construir um esquema multidimensional;
- Preparar o modelo para análise OLAP.

**Modelo inicial proposto:**
- Dimensão Tempo;
- Dimensão Localização;
- Dimensão Nível de Tensão;
- Facto Consumo de Energia.

A utilização de indicadores anuais complementares poderá exigir uma tabela de factos adicional, evitando agregações incorretas entre dados de granularidades diferentes.

**Resultado esperado:** modelo multidimensional documentado e funcional para análise.

### Fase 4 — Business Intelligence e análise OLAP

**Objetivo:** explorar os dados e produzir informação analítica.

Atividades:
- Construir tabelas dinâmicas;
- Criar gráficos e indicadores;
- Analisar tendências de consumo;
- Comparar municípios e períodos;
- Aplicar operações OLAP;
- Interpretar os resultados obtidos.

Pretende-se demonstrar operações como:
- **Roll-up:** agregação de informação;
- **Drill-down:** análise de maior detalhe;
- **Slice:** seleção de uma dimensão;
- **Dice:** aplicação de filtros multidimensionais;
- **Pivot:** alteração da perspetiva de análise.

**Resultado esperado:** análises interativas que permitam responder às questões do estudo.

### Fase 5 — Validação e documentação

**Objetivo:** garantir a correção técnica e documentar o trabalho realizado.

Atividades:
- Verificar a consistência dos dados;
- Validar os cálculos e resultados;
- Documentar o processo ETL;
- Explicar o modelo multidimensional;
- Descrever as técnicas de análise;
- Identificar limitações;
- Redigir o relatório técnico;
- Registar e declarar a utilização de IA, nos termos do enunciado.

**Resultado esperado:** relatório técnico e documentação do projeto.

### Fase 6 — Demonstração e apresentação

**Objetivo:** demonstrar o funcionamento da solução e apresentar as conclusões.

Atividades:
- Preparar os materiais de apresentação;
- Gravar vídeo(s) demonstrativos das análises;
- Explicar as operações OLAP realizadas;
- Apresentar os principais resultados;
- Preparar a defesa das decisões técnicas;
- Organizar a entrega final.

**Resultado esperado:** projeto documentado, vídeo(s) de demonstração e entrega final.

## 7. Organização do repositório

A estrutura prevista é a seguinte:

| Diretório | Finalidade |
|---|---|
| `docs/` | Documentação, planeamento, decisões e relatório |
| `data/raw/` | Datasets originais |
| `data/processed/` | Dados tratados e preparados |
| `etl/` | Scripts e recursos do processo ETL |
| `database/` | Modelo multidimensional e scripts SQL |
| `analysis/` | Análises, gráficos e ficheiros BI |
| `presentation/` | Apresentação e recursos demonstrativos |
| `README.md` | Apresentação e organização do projeto |

Esta estrutura poderá ser ajustada em função das ferramentas selecionadas. Os dados de grande dimensão e ficheiros gerados automaticamente não deverão ser adicionados indiscriminadamente ao repositório.

## 8. Organização da equipa

O trabalho será realizado por um grupo de três estudantes.

| Elemento | Responsabilidades propostas |
|---|---|
| Elemento 1 | Pesquisa, caracterização das fontes e preparação ETL |
| Elemento 2 | Modelação multidimensional e organização dos dados |
| Elemento 3 | Análise BI, operações OLAP e visualizações |

Esta distribuição é apenas uma proposta de organização inicial.

**Todas as fases deverão ser acompanhadas e compreendidas pelos três elementos.** A validação dos resultados, a elaboração do relatório e a preparação da apresentação serão responsabilidades partilhadas.

## 9. Gestão do desenvolvimento com GitHub

O GitHub será utilizado para o controlo de versões, organização de tarefas e colaboração entre os elementos do grupo.

### Estrutura de branches

- `main` — versão principal e estável;
- `develop` — integração do trabalho em desenvolvimento;
- `feature/*` — implementação de funcionalidades e componentes;
- `docs/*` — criação e atualização de documentação;
- `fix/*` — correção de problemas identificados.

### Fluxo de trabalho

1. Criar uma tarefa ou identificar uma alteração necessária.
2. Criar uma branch a partir de `develop`.
3. Realizar e testar as alterações.
4. Criar commits com mensagens descritivas.
5. Abrir um Pull Request para `develop`.
6. Solicitar a revisão de outro elemento.
7. Integrar as alterações após validação.
8. Atualizar a documentação, quando necessário.

### Convenção de commits

Exemplos:
- `docs: add project overview`
- `docs: define analysis questions`
- `feat: add energy data extraction`
- `feat: implement dimensional model`
- `feat: add OLAP analysis`
- `fix: correct data transformation`

## 10. Planeamento e acompanhamento

O desenvolvimento será acompanhado através das tarefas e Issues do GitHub.

| Fase | Estado inicial |
|---|---|
| Definição e exploração dos dados | Em desenvolvimento |
| ETL | Por iniciar |
| Modelo multidimensional | Por iniciar |
| Análise BI e OLAP | Por iniciar |
| Documentação e validação | Por iniciar |
| Demonstração e entrega | Por iniciar |

As prioridades e os prazos serão definidos em grupo, tendo em conta a data de entrega estabelecida pela docente.

## 11. Tecnologias e ferramentas

As tecnologias ainda não estão definitivamente selecionadas.

| Finalidade | Ferramentas em consideração |
|---|---|
| Tratamento de dados | Python, Pandas, Power Query |
| Base de dados | PostgreSQL |
| Modelação multidimensional | SQL, diagramas ER/dimensionais |
| Business Intelligence | Microsoft Power BI |
| Controlo de versões | Git e GitHub |
| Documentação | Markdown |

A escolha final deverá considerar a complexidade do projeto, os recursos disponíveis e a capacidade de demonstrar as operações exigidas no enunciado.

## 12. Critérios de avaliação

De acordo com o enunciado do Trabalho Prático n.º 1:

| Componente | Peso |
|---|---:|
| Processo ETL | 20% |
| Modelo multidimensional | 20% |
| Técnicas de análise BI e OLAP | 40% |
| Relatório técnico | 10% |
| Originalidade | 10% |

A prioridade será garantir a correção do processo de tratamento e integração dos dados, a adequação do modelo multidimensional e a qualidade das análises desenvolvidas.

## 13. Utilização de Inteligência Artificial

A utilização de ferramentas de IA será realizada de acordo com as regras definidas no enunciado.

Todas as contribuições relevantes de IA deverão ser registadas, analisadas e verificadas pelos elementos do grupo.

O relatório incluirá uma **Declaração de Uso de IA**, com a identificação das ferramentas utilizadas, tarefas apoiadas, prompts e procedimentos de verificação humana.

O processo de utilização de IA e as decisões tomadas deverão ficar documentados e ser partilhados conforme as instruções da docente.

## 14. Equipa

**Licenciatura em Engenharia Informática — UPBeja**

**Unidade Curricular:** Sistemas de Informação

**Ano letivo:** 2026/2027

**Trabalho Prático:** n.º 1 — Energia

**Elementos do grupo:**
- Beatriz Caixeiro
- Eduardo Madeira
- Francisco Soudo
