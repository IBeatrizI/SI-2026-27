"""Testes do descarregador com respostas simuladas (sem chamadas à E-REDES)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DIR/'scripts'))
import descarregar_e_redes as download


class TestDownloader(unittest.TestCase):
    def test_api_url(self):
        u = download.api_url('exports/csv', where="ano = '2024'", delimiter=';')
        self.assertIn('/exports/csv?',u)
        self.assertIn('ano+%3D+%272024%27',u)

    def test_verify_source_csv(self):
        csv_path = DIR/'tests'/'fixtures'/'e_redes_sintetico_2024.csv'
        count, delim=download.verify_csv(csv_path, 2024)
        self.assertEqual(count, 5)
        self.assertEqual(delim, ';')
        with self.assertRaises(ValueError):
            download.verify_csv(csv_path, 2023)

    def test_mocked_download_with_reconciliation(self):
        csv_path = DIR/'tests'/'fixtures'/'e_redes_sintetico_2024.csv'
        synthetic=csv_path.read_bytes()
        mocked_count=json.dumps({'total_count':5,'results':[]}).encode()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(download,'request_bytes',side_effect=[mocked_count, synthetic]):
                meta=download.download_year(2024, Path(tmp), substituir=False)
            self.assertEqual(meta['linhas'], 5)
            self.assertEqual(meta['contagem_api'], 5)
            self.assertTrue((Path(tmp)/'e_redes_consumos_concelho_2024.csv').exists())
            self.assertTrue((Path(tmp)/'e_redes_consumos_concelho_2024.meta.json').exists())

    def test_incomplete_download_rejected(self):
        csv_path = DIR/'tests'/'fixtures'/'e_redes_sintetico_2024.csv'
        synthetic=csv_path.read_bytes()
        mocked_count=json.dumps({'total_count':99,'results':[]}).encode()
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(download,'request_bytes',side_effect=[mocked_count, synthetic]):
                with self.assertRaises(ValueError):
                    download.download_year(2024,Path(tmp),substituir=False)
            self.assertFalse((Path(tmp)/'e_redes_consumos_concelho_2024.csv').exists())

if __name__ == '__main__':
    unittest.main()
