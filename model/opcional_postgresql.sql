-- Esquema opcional de Data Warehouse em PostgreSQL.
-- Esquema SQL opcional, AINDA NÃO EXECUTADO no PostgreSQL; os CSVs já foram produzidos com dados reais.
-- Todos os CSV gerados pelo ETL têm cabeçalho, UTF-8 BOM e delimitador ",".
BEGIN;
CREATE SCHEMA IF NOT EXISTS energia_dw;
CREATE TABLE IF NOT EXISTS energia_dw.dim_tempo (
  id_tempo integer PRIMARY KEY,
  ano integer NOT NULL,
  mes integer NOT NULL CHECK (mes BETWEEN 1 AND 12),
  trimestre integer NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
  semestre integer NOT NULL CHECK (semestre BETWEEN 1 AND 2),
  nome_mes text NOT NULL,
  ano_mes text NOT NULL
);
CREATE TABLE IF NOT EXISTS energia_dw.dim_municipio (
  id_municipio varchar(120) PRIMARY KEY,
  codigo_municipio varchar(4),
  concelho text NOT NULL,
  codigo_distrito varchar(2),
  distrito text NOT NULL,
  tipo_localizacao varchar(40) NOT NULL
    CHECK (tipo_localizacao IN ('municipio', 'agregado_rgpd', 'sem_codigo'))
);
CREATE TABLE IF NOT EXISTS energia_dw.dim_tensao (
  id_tensao varchar(120) PRIMARY KEY,
  nivel_tensao text NOT NULL
);
CREATE TABLE IF NOT EXISTS energia_dw.fact_consumo_mensal (
  id_tempo integer NOT NULL REFERENCES energia_dw.dim_tempo(id_tempo),
  id_municipio varchar(120) NOT NULL REFERENCES energia_dw.dim_municipio(id_municipio),
  id_tensao varchar(120) NOT NULL REFERENCES energia_dw.dim_tensao(id_tensao),
  consumo_kwh numeric(28,6) NOT NULL,
  PRIMARY KEY (id_tempo, id_municipio, id_tensao)
);
CREATE INDEX IF NOT EXISTS ix_fact_municipio ON energia_dw.fact_consumo_mensal(id_municipio);
CREATE INDEX IF NOT EXISTS ix_fact_tensao ON energia_dw.fact_consumo_mensal(id_tensao);
COMMIT;
-- A ordem de importação deve ser dimensões -> factos.
-- Não somar rácios per capita. Não executar INSERTs com dados de teste como se fossem reais.
