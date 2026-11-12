# Medidas DAX propostas

Adicionar as medidas ao Power BI após validar os tipos e as relações. Não são resultados reais; são fórmulas sugeridas para análise.

```dax
Consumo (kWh) =
SUM(FactConsumoMensal[consumo_kwh])
```

```dax
Consumo (MWh) =
DIVIDE([Consumo (kWh)], 1000)
```

```dax
Consumo Municipal (kWh) =
CALCULATE(
    [Consumo (kWh)],
    DimMunicipio[tipo_localizacao] = "municipio"
)
```

```dax
Consumo Ano Anterior (kWh) =
SUMX(
    VALUES(DimTempo[id_tempo]),
    VAR PeriodoAnterior = DimTempo[id_tempo] - 100
    RETURN
        CALCULATE(
            [Consumo (kWh)],
            REMOVEFILTERS(DimTempo),
            DimTempo[id_tempo] = PeriodoAnterior
        )
)
```

```dax
Variação Homóloga (%) =
DIVIDE(
    [Consumo (kWh)] - [Consumo Ano Anterior (kWh)],
    [Consumo Ano Anterior (kWh)]
)
```

**Interpretação:** `id_tempo = AAAAMM`; subtrair 100 corresponde ao mesmo mês do ano anterior. Esta abordagem não depende de tratar `DimTempo` como tabela de datas **diária**, o que seria incorreto no modelo mensal. Confirmar resultados com uma matriz por período e consultar os casos em que o período anterior não existe.

**Evitar:** somar valores `kWh/habitante` da PORDATA. Para agregações territoriais, é necessário um rácio calculado a partir dos consumos e populações compatíveis, não uma soma ou média simples de rácios municipais.
