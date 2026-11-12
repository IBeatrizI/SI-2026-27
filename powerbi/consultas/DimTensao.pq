let
    Fonte = Csv.Document(File.Contents(pDataFolder & "\dim_tensao.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalhos, {{"id_tensao", type text}, {"nivel_tensao", type text}}, "en-US")
in
    Tipos
