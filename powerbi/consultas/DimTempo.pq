let
    Fonte = Csv.Document(File.Contents(pDataFolder & "\dim_tempo.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalhos, {{"id_tempo", Int64.Type}, {"ano", Int64.Type}, {"mes", Int64.Type}, {"trimestre", Int64.Type}, {"semestre", Int64.Type}, {"nome_mes", type text}, {"ano_mes", type text}}, "en-US")
in
    Tipos
