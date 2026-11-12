# Histórico de alterações (CHANGELOG)

## Fase 2 — 12/11/2026

### Implementado e validado

- Recolha E-REDES (2021–2024), com manifesto de proveniência.
- ETL dos consumos por município e nível de tensão, com três dimensões e uma tabela de factos.
- Verificações de integridade e reconciliação independente dos consumos faturados.
- Seis tabelas analíticas e indicadores preliminares calculados dos dados reais.
- Dez testes automáticos aprovados com dados **sintéticos**.

### Organização para GitHub

- README principal reescrito, com estado, âmbito, arquitetura, execução e pendências.
- Instruções de arranque unificadas em `docs/GUIA_EXECUCAO.md` e índice `docs/README.md`.
- Guia completo de primeira submissão e Pull Request para `develop`.
- Ficheiros grandes (`data/raw/`, `data/processed/`) excluídos do Git por omissão.
- Resultados leves e relatórios de qualidade incluídos para consulta.
- Manifesto dos CSVs originais guardado em `docs/12_manifesto_recolha_e_redes.json`.
- Execução de `INICIAR_WINDOWS.bat` alargada à validação independente e geração de análises.
- Regularização de fins de linha com `.gitattributes`.

### Ainda por implementar

- Importação e validação do modelo num PBIX, dashboards e operações OLAP.
- Integração dos dados anuais DGEG e PORDATA.
- Relatório académico, demonstração em vídeo e Declaração de Uso de IA.

**Nota:** este documento descreve o estado da Fase 2, não uma versão final do trabalho.
