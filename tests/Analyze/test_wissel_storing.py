import unittest
import pandas as pd
from datetime import datetime
from Run.core.Analyze.wissel_storing import wissel_storing

class TestWisselStoring(unittest.TestCase):

    def setUp(self):
        self.base_time = datetime(2024, 1, 1, 12, 0, 0)

    def create_dataframe(self, voertuig_nr, fifo_level):
        return pd.DataFrame([
            {'date-time': self.base_time, 'wissel nr': 101, '<aanmelden> lijn': '3',
             '<aanmelden> service': 'A', '<aanmelden> categorie': 'Normaal',
             '<aktuell> voertuig': voertuig_nr, '<aktuell> niveau fifo': fifo_level},
            {'date-time': self.base_time, 'wissel nr': 101, '<aanmelden> lijn': '3',
             '<aanmelden> service': 'A', '<aanmelden> categorie': 'Normaal',
             '<aktuell> voertuig': voertuig_nr, '<aktuell> niveau fifo': fifo_level}
        ])

    def test_voertuig_present_returns_minus_one(self):
        df = self.create_dataframe(voertuig_nr=4001, fifo_level=2)
        result = wissel_storing(df)
        self.assertEqual(result, -1)

    def test_voertuig_zero_returns_error_dataframe(self):
        df = self.create_dataframe(voertuig_nr=0, fifo_level=5)
        result = wissel_storing(df)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result['Error type'][0], 'voertuig nummer aanmelden fout')
        self.assertEqual(result['Veroozak'][0], 'Tram Vecom system')

    def test_dataframe_output_columns(self):
        df = self.create_dataframe(voertuig_nr=0, fifo_level=3)
        result = wissel_storing(df)
        expected_columns = ['Begin tijd', 'Eind tijd', 'Wissel nr', 'lijn', 'service', 'categorie', 'voertuig', 'fifo', 'Error type', 'Veroozak']
        for col in expected_columns:
            self.assertIn(col, result.columns)

if __name__ == '__main__':
    unittest.main()
