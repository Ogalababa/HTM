import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os

# 当前文件所在目录
rootPath = os.path.abspath(os.path.dirname(__file__))

from Run.core.Integration.DataCalculator import Calculator


class TestCalculator(unittest.TestCase):

    @patch('Run.core.Integration.DataCalculator.get_alldata_from_db')
    def setUp(self, mock_get_data):
        # 模拟数据库返回值
        mock_df = pd.DataFrame({
            'date-time': pd.date_range('2024-01-01', periods=5, freq='min'),
            'step': [1, 2, 3, 4, 5]
        })
        mock_get_data.return_value = {'W001': mock_df}
        self.calc = Calculator(db_name='test_db')

    def test_get_wissel_cycles(self):
        df = pd.DataFrame({
            'date-time': pd.date_range('2024-01-01', periods=5, freq='min'),
            'step': [1, 2, 3, 4, 5]
        })
        with patch('Run.core.Integration.DataCalculator.wissel_cycle_list', return_value=[0, 5]):
            cycles = self.calc.get_wissel_cycles(df)
            self.assertEqual(len(cycles), 1)
            self.assertTrue(isinstance(cycles[0], pd.DataFrame))

    @patch('Run.core.Integration.DataCalculator.save_to_sql')
    @patch('Run.core.Integration.DataCalculator.calculation_tram_speed')
    @patch('Run.core.Integration.DataCalculator.wissel_cycle_list', return_value=[0, 5])
    def test_sub_tram_speed(self, mock_cycle_list, mock_speed_calc, mock_save):
        mock_speed_calc.return_value = [pd.DataFrame({'speed': [10]})]
        self.calc.sub_tram_speed_('W001')
        mock_save.assert_called_once()

    @patch('Run.core.Integration.DataCalculator.save_to_sql')
    @patch('Run.core.Integration.DataCalculator.wissel_schakel')
    @patch('Run.core.Integration.DataCalculator.check_storing_df', return_value=False)
    @patch('Run.core.Integration.DataCalculator.wissel_cycle_list', return_value=[0, 5])
    def test_sub_wissel_schakel(self, mock_cycle, mock_check, mock_switch, mock_save):
        mock_switch.return_value = [pd.DataFrame({'status': [1]})]
        self.calc.sub_wissel_schakel_('W001')
        mock_save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
