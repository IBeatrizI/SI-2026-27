"""Testes locais: a fixture é inteiramente SINTÉTICA e nunca é um resultado real."""
import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
from preparar_dw import build, parse_decimal
from validar_dw import validate

class TestEnergyETL(unittest.TestCase):
    def test_decimal(self):
        self.assertEqual(parse_decimal('123,45'), Decimal('123.45'))
        self.assertEqual(parse_decimal('-5.00'), Decimal('-5.00'))
        with self.assertRaises(ValueError): parse_decimal('1.234,56')

    def test_aggregation_and_rgpd(self):
        fixture=Path(__file__).resolve().parent/'fixtures'/'e_redes_sintetico_2024.csv'
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)
            report=build([fixture], dest/'processed', dest/'quality')
            self.assertEqual(report['linhas_fonte'], 5)
            self.assertEqual(report['linhas_facto'], 4)
            self.assertEqual(Decimal(report['soma_bruta_kwh']),Decimal('165.75'))
            self.assertEqual(report['linhas_outros_rgpd'],1)
            self.assertEqual(report['linhas_consumo_negativo'],1)
            with (dest/'processed'/'fact_consumo_mensal.csv').open(encoding='utf-8-sig') as f:
                rows=list(csv.DictReader(f))
            self.assertEqual(len(rows),4)
            main=[r for r in rows if r['id_tempo']=='202401' and r['id_municipio']=='0205' and r['id_tensao']=='BAIXA_TENSAO']
            self.assertEqual(Decimal(main[0]['consumo_kwh']), Decimal('150.75'))
            check=validate(dest/'processed',dest/'quality')
            self.assertEqual(check['factos'],4)

    def test_invalid_year_fails(self):
        header='ano;mes;data;distrito;concelho;freguesia;nivel_de_tensao;energia_ativa_kwh;coddistrito;coddistritoconcelho;coddistritoconcelhofreguesia;mes_int\n'
        line='2024;13;2024-13;Beja;Beja;X;Baixa Tensão;1;02;0205;020501;13\n'
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'wrong.csv'
            path.write_text(header+line,encoding='utf-8')
            with self.assertRaises(ValueError): build([path],Path(folder)/'out',Path(folder)/'quality')
            self.assertFalse((Path(folder)/'out'/'fact_consumo_mensal.csv').exists())

if __name__=='__main__': unittest.main()
