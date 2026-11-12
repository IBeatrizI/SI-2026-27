# Recolha e execução reproduzível (Windows)

## Pré-requisitos

- Python 3.10 ou superior (`py --version`), com acesso à Internet para descarregar.
- Power BI Desktop instalado apenas para a fase posterior de visualização.
- Sem bibliotecas Python adicionais: os scripts utilizam apenas a biblioteca padrão.

## 1. Verificar os scripts

Na raiz do projeto:

```powershell
py -m unittest discover -s tests -v
```

Os testes usam **apenas dados sintéticos**, não demonstram resultados do estudo. Podem correr sem Internet.

## 2. Descarregar os dados reais

```powershell
py scripts/descarregar_e_redes.py --anos 2021 2022 2023 2024
```

A API usada é a **Explore API v2.1**. Para cada ano o programa:

1. Pergunta ao endpoint `/records` quantos registos existem para `ano = 'YYYY'`.
2. Exporta o ano pelo endpoint `/exports/csv`.
3. Rejeita CSVs com cabeçalhos errados, ano inesperado ou número de linhas diferente da API.
4. Guarda o CSV original e um JSON de proveniência com URL, data UTC, número de linhas e hash SHA-256.
5. Não substitui ficheiros anteriores a menos que se acrescente `--substituir`.

**Nota:** a E-REDES atualiza os dados, pelo que uma segunda descarga pode dar resultados diferentes. Essa alteração é legítima mas deve ser documentada. O controlo de contagens protege contra uma exportação incompleta; não prova, por si só, a ausência de inconsistências na origem.

### Se a API não responder

- Confirmar a Internet e abrir o [portal E-REDES](https://e-redes.opendatasoft.com/explore/dataset/3-consumos-faturados-por-municipio-ultimos-10-anos/export/).
- Exportar separadamente cada ano com filtro `ano`, preferencialmente em CSV completo (não usar apenas as linhas visíveis da tabela).
- Verificar colunas, ano, número de linhas e unidades.
- Guardar os ficheiros em `data/raw/e_redes/` com os nomes exatos `e_redes_consumos_concelho_2021.csv`, ..., `_2024.csv`.
- Executar `py scripts/perfil_e_redes.py` para inspecionar; **sem metadados automáticos, registar manualmente URL/data/contagem e calcular SHA-256**.
- Para calcular um hash no PowerShell: `Get-FileHash .\data\raw\e_redes\e_redes_consumos_concelho_2024.csv -Algorithm SHA256`.

## 3. Analisar a qualidade dos dados originais

```powershell
py scripts/perfil_e_redes.py
```

Registar total de linhas, cobertura temporal, categorias de tensão, códigos em falta, agregados RGPD (`OUTROS`) e consumos negativos. Não apagar nulos nem negativos automaticamente.

## 4. ETL e controlo da reconciliação

```powershell
py scripts/preparar_dw.py
py scripts/validar_dw.py
```

**Não executar esta fase se os CSVs estiverem incompletos.** O programa deteta vários erros e falha antes de escrever dados no caso de valores ou períodos incoerentes. Depois de executar, inspecionar `data/quality/relatorio_etl.json`. A soma dos `consumo_kwh` no facto tem de ser exatamente igual à soma válida de `energia_ativa_kwh` da origem, incluindo negativos e categoria RGPD.

Requisitos para considerar a fase concluída:

- [ ] Todos os 48 meses de 2021–2024 presentes.
- [ ] Contagens de registos conferidas na API ou verificadas manualmente.
- [ ] Sem erros de cabeçalho, datas, tipos numéricos ou relações.
- [ ] `diferenca_kwh = 0` no relatório ETL.
- [ ] Registos `OUTROS` e sem código quantificados.
- [ ] Qualquer conflito de nomenclatura de município resolvido/documentado.
- [ ] Resultados conferidos por outro elemento do grupo.

## 5. Próxima etapa

Abrir `powerbi/GUIA_POWER_BI.md`, criar um PBIX **novo** e importar as quatro tabelas geradas. DGEG e PORDATA só são integradas quando as regras de harmonização estiverem validadas.
