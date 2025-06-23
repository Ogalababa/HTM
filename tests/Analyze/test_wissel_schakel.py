import unittest
import pandas as pd
from datetime import datetime
from Run.core.Analyze.wissel_schakel import wissel_schakel

class TestWisselSchakel(unittest.TestCase):

    def setUp(self):
        self.base_time = datetime(2024, 1, 1, 12, 0, 0)

    def create_dataframe(self, rows):
        return pd.DataFrame(rows)


    def test_output_structure(self):
        df = self.create_dataframe([
            {'date-time': self.base_time, 'wissel nr': 105, '<aktuell> voertuig': 4003,
             '<wissel> links': 1, '<input> naar rechts': 1},
            {'date-time': self.base_time, 'wissel nr': 105, '<wissel> rechts': 1, '<aktuell> voertuig': 4003}
        ])
        result = wissel_schakel(df)
        self.assertIn('Tijd', result[0].columns)
        self.assertIn('Wissel Nr', result[0].columns)
        self.assertIn('voertuig Nr', result[0].columns)
        self.assertIn('Schakelen', result[0].columns)
        self.assertIn('Voor', result[0].columns)
        self.assertIn('Na', result[0].columns)
        self.assertIn('aanvragen', result[0].columns)

if __name__ == '__main__':
    unittest.main()
