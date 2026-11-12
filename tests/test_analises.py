import unittest
from decimal import Decimal
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from gerar_analises import growth,fmt

class TestAnalises(unittest.TestCase):
    def test_growth(self):
        self.assertEqual(growth(Decimal('105'),Decimal('100')),'5.0000')
    def test_no_previous_year(self):
        self.assertEqual(growth(Decimal('105'),None),'')
        self.assertEqual(growth(Decimal('105'),Decimal('0')),'')
    def test_round_kwh(self):
        self.assertEqual(fmt(Decimal('0.123456')),'0.123')
