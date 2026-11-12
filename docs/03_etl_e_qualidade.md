# Processo ETL e critérios de qualidade

## Extract

Fonte principal: dados de consumos **mensais faturados** da E-REDES, exportados separadamente para 2021, 2022, 2023 e 2024. Ficheiros originais mantidos sem edição em `data/raw/e_redes`. Hash e contagem guardados nos `.meta.json`.

## Transform

| Operação | Implementação | Razão |
|---|---|---|
| Tipos | `ano`/`mes_int` → inteiros; energia → `Decimal` | Evitar soma em texto e erros de arredondamento |
| Consistência temporal | Ano, mês, data e ano no nome do ficheiro | Detetar exportações ou linhas erradas |
| Códigos | Preservar como texto de largura 2/4 | Não perder zeros iniciais |
| Conservação dos valores | Manter consumos negativos | Podem refletir acertos de faturação; não inventar correções |
| RGPD | `OUTROS` → membro territorial agregado por distrito | Preservar totais sem atribuição indevida a município |
| Granularidade | Agregar freguesias para mês × município × tensão | Preparar factos para análises municipais |
| Chaves | Gerar dimensões de tempo, município/agregado e tensão | Modelo em estrela |
| Reconciliação | Comparar soma `Decimal` antes/depois | Evitar duplicação ou perda de kWh |
| Qualidade | Contagens, nulos, ausência de meses, conflitos de nomes | Preparar relatório técnico e decisões auditáveis |

O ETL não completa automaticamente valores em falta, não cria municípios e não elimina consumos negativos. Registos com valores fundamentais inválidos provocam erro e interrompem a escrita. Casos sem código territorial válido são mantidos e assinalados para investigação.

**Limitação conhecida:** o procedimento identifica possíveis conflitos de nomenclatura, mas não implementa gestão histórica de nomes de municípios. O grupo deve rever os avisos e justificar a estratégia escolhida.

## Load

O script cria CSVs modelados em `data/processed/`, adequados para importação no Power BI. Opcionalmente, podem ser carregados numa base PostgreSQL usando `model/opcional_postgresql.sql`, após validação da correspondência de tipos. O Data Warehouse é uma proposta multidimensional; o uso de um SGBD específico não é exigência explícita do enunciado.

## Evidências necessárias no relatório

1. Capturas ou descrição de esquema original, tipos e contagens, **retiradas de execução real**.
2. Regras de transformação, com justificação e exemplos reais quando disponíveis.
3. Controlo de qualidade (nulos/negativos/RGPD/meses).
4. Reconciliação de totais fonte→facto.
5. Limitações, atualizações da fonte e diferenças de granularidade.

**Não usar os valores dos testes sintéticos como resultados do estudo.**
