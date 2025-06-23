import unittest
import pandas as pd
from Run.core.Analyze import check_storing_df as cs


class TestCheckStoringDf(unittest.TestCase):
    def setUp(self):
         
        self.valid_df = pd.DataFrame({
            '<wissel> vergrendeld': [1, 1, 1],
            '<wissel> ijzer': [1, 1, 1],
            '<vecom> aanvraag onbekend': [1, 1, 1],
            '<vecom> storing': [0, 0, 0],
            '<vecom> geen output': [0, 0, 0],
            '<aanmelden> voertuig': [1001, 1001, 1002],
            'date-time': pd.date_range('2024-01-01', periods=3, freq='min')
        })

         
        self.invalid_df = pd.DataFrame({
            '<wissel> vergrendeld': [0, 0, 0],
            '<wissel> ijzer': [0, 0, 0],
            '<vecom> aanvraag onbekend': [0, 0, 0],
            '<vecom> storing': [0, 0, 0],
            '<vecom> geen output': [0, 0, 0],
            '<aanmelden> voertuig': [0, 0, 0],
            'date-time': pd.date_range('2024-01-01', periods=3, freq='min')
        })

         
        self.recheck_df = pd.DataFrame({
            '<wissel> vergrendeld': [1, 1, 0, 1],
            '<wissel> ijzer': [1, 0, 0, 1],
            '<hfp> spoorstroomkring bezet': [1, 0, 1, 0],
            '<hfk> aanwezigheidslus bezet': [1, 1, 0, 0],
            '<aktuell> niveau fifo': [0, 0, 1, 1],
            '<aktuell> voertuig': [0, 0, 0, 0],
            '<aanmelden> voertuig': [1001, 1002, 1001, 1002],
            '<aanmelden> lijn': [2, 3, 2, 3],
            'wissel nr': ['W100', 'W100', 'W100', 'W100'],
            'step': [0, 1, 2, 1],
            'date-time': pd.date_range('2024-01-01', periods=4, freq='min')
        })

    def test_check_storing_df_returns_true(self):
        result = cs.check_storing_df(self.valid_df)
        self.assertTrue(result)



if __name__ == '__main__':
    unittest.main()
