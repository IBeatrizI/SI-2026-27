let
    Fonte = Csv.Document(File.Contents(pDataFolder & "\dim_municipio.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipos = Table.TransformColumnTypes(Cabecalhos, {{"id_municipio", type text}, {"codigo_municipio", type text}, {"concelho", type text}, {"codigo_distrito", type text}, {"distrito", type text}, {"tipo_localizacao", type text}}, "en-US")
in
    Tipos
