# Fase 3 — Integração de fontes complementares (por implementar)

O enunciado valoriza **dados de várias fontes e formatos**. O núcleo E-REDES (mensal, kWh faturados) já está preparado. Antes de afirmar que concluímos o ETL multifonte, temos de importar e validar **DGEG** e **PORDATA** com dados reais.

## DGEG — Consumo de eletricidade por município e setor de atividade

Fonte oficial: https://www.dgeg.gov.pt/pt/estatistica/energia/eletricidade/consumo-por-municipio-e-setor-de-atividade/

O portal dispõe de Excel por ano, atualmente com 2021–2024 indicados como **provisórios**. Descarregar manualmente os quatro ficheiros e preservá-los sem alteração em `data/raw/dgeg/`:

- [2021](https://www.dgeg.gov.pt/media/fq5naru4/dgeg-eca-2021.xlsx)
- [2022](https://www.dgeg.gov.pt/media/okcmesq3/dgeg-eca-2022.xlsx)
- [2023](https://www.dgeg.gov.pt/media/c4shghov/dgeg-eca-2023.xlsx)
- [2024](https://www.dgeg.gov.pt/media/iqxczkj0/dgeg-eca-2024.xlsx)

**Não construir o ETL definitivo sem examinar os livros Excel**, nomeadamente a(s) folha(s), cabeçalhos, unidades, categorias CAE, linhas de totais e códigos oficiais dos municípios. Os anos devem ser validados separadamente — o formato pode mudar.

Estrutura multidimensional **proposta**: `FactConsumoSetorialAnual` com granularidade `ano × municipio × setor` e medidas em kWh (converter unidades **apenas quando confirmadas**). Dimensões: `DimAno`, `DimMunicipio` (códigos harmonizados) e `DimSetor`.

**Risco de dupla contagem:** não somar linhas agregadas por distrito/NUTS com os municípios, nem totais gerais com setores detalhados. Não somar os factos DGEG aos factos E-REDES, pois podem medir universos semelhantes sem identidades estritas.

## PORDATA — Consumo por habitante

Fonte oficial: https://www.pordata.pt/municipios/consumo+de+energia+eletrica+por+habitante+total+e+por+tipo+de+consumo-435

Exportar para Excel a tabela municipal, registar a data de acesso e confirmar 2021–2024 e os tipos de consumo escolhidos. A PORDATA indica atualização em 24/06/2026, incluindo revisão de estimativas populacionais de 2021–2024.

Estrutura **proposta**: `FactConsumoPerCapitaAnual`, com granularidade `ano × municipio × indicador`; medida **kWh/hab.**. Não **somar** rácios per capita entre anos ou municípios. Para obter médias agregadas, dispor da população correspondente por ano, e calcular quociente entre totais compatíveis.

## Critérios de aceitação para a integração

- Registar a proveniência, URL, data de download, licença e SHA256 de cada ficheiro.
- Verificar esquema, períodos, valores nulos, códigos geográficos, unidades e categorias agregadas.
- Documentar qualquer mapeamento de códigos municipais e a versão administrativa usada.
- Manter **factos separados**, com dimensões conformadas apenas onde os códigos e definições forem compatíveis.
- Validar totais por ano e município contra cada fonte original antes de publicar um dashboard integrado.
- Criar relatório técnico comparando cobertura e definições das três fontes; a PORDATA pode utilizar DGEG/INE como fontes primárias.

**Estado efetivo:** os ficheiros DGEG/PORDATA **não** foram importados neste pacote. O ambiente de execução não conseguiu descarregar os Excel da DGEG; estes links foram obtidos da página oficial. Não se inventaram dados para simular essa integração.
