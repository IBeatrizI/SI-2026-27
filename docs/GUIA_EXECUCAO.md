# Guia de execução — Fase 2 (Windows)

Este projeto contém os **scripts que já foram executados e validados com CSVs reais da E-REDES**. O GitHub inclui o **manifesto de proveniência** e alguns resultados leves, mas não inclui os 4 CSVs originais nem os factos processados. O arquivo local completo contém-nos e permite continuar sem descarregar.

## Pré-requisitos

1. Instalar Python 3.10 ou superior e confirmar no **PowerShell**: `py --version`.
2. Clonar ou extrair o projeto e abrir a pasta **raiz** (a que contém `README.md` e `INICIAR_WINDOWS.bat`).
3. Para os dashboards, instalar Power BI Desktop (não é necessário para executar os scripts Python).

## A — Primeira execução, a partir do GitHub

No PowerShell, na raiz do projeto:

```powershell
py -m unittest discover -s tests -v
.\INICIAR_WINDOWS.bat
```

O executável realiza, pela ordem: testes automáticos com dados sintéticos, download dos quatro anos 2021–2024, perfil, ETL, validação das dimensões e factos, reconciliação independente com os CSVs originais e geração dos resultados exploratórios.

**Internet necessária:** para chamar a API da E-REDES. A fonte pode ter sido revista desde 12/11/2026. Se as contagens ou totais diferirem do snapshot do README, documentar a nova data e os resultados, sem forçar a coincidência.

## B — Continuar sem novo download

Se existem os 4 CSVs originais na pasta `data/raw/e_redes/`, executar:

```powershell
.\CONTINUAR_WINDOWS.bat
```

Alternativamente, os comandos equivalentes são:

```powershell
py -m unittest discover -s tests -v
py scripts/perfil_e_redes.py
py scripts/preparar_dw.py
py scripts/validar_dw.py
py scripts/validar_origem_e_dw.py
py scripts/gerar_analises.py
```

## C — O que verificar depois

- `data/raw/e_redes/`: quatro CSVs e respetivos `.meta.json` (quando descarregados pelo script);
- `data/processed/`: `dim_tempo.csv`, `dim_municipio.csv`, `dim_tensao.csv`, `fact_consumo_mensal.csv`;
- `data/quality/relatorio_etl.json`: contagens, totais, valores negativos e localização RGPD;
- `data/quality/validacao_independente.json`: diferenças por mês × distrito × tensão;
- `data/analysis/`: tabelas exploratórias reais em CSV e indicadores JSON.

O ficheiro [`12_manifesto_recolha_e_redes.json`](12_manifesto_recolha_e_redes.json) guarda os hashes e contagens dos **originais da execução de 12/11/2026** e permite verificar se os ficheiros atuais pertencem ao mesmo snapshot.

## D — Abrir no Power BI

Depois de validar os CSVs, seguir [`../powerbi/GUIA_POWER_BI.md`](../powerbi/GUIA_POWER_BI.md). O modelo precisa de ser importado e validado pelo grupo; não existe PBIX construído no pacote.

## E — Resolução de problemas

- Se `py` não for reconhecido, instalar Python e ativar o Python Launcher (ou adaptar os comandos para `python`).
- Se a API falhar, verificar a ligação e consultar [`02_recolha_e_execucao.md`](02_recolha_e_execucao.md).
- Se a validação reprovar, **não utilizar os resultados em gráficos** antes de investigar a causa.
- Não editar os CSVs brutos. Não copiar os ficheiros `data/raw/` para o GitHub: são gerados localmente e são ignorados pelo Git.
