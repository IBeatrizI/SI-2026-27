let
    Fonte = Csv.Document(File.Contents(pDataFolder & "\fact_consumo_mensal.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalhos, {{"id_tempo", Int64.Type}, {"id_municipio", type text}, {"id_tensao", type text}, {"consumo_kwh", type number}}, "en-US")
in
    Tipos
