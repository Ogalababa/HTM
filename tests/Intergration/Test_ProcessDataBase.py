import unittest
from unittest.mock import patch, MagicMock
from Run.core.Integration.ProcessDataBase import process_db


class TestProcessDataBase(unittest.TestCase):

    @patch('Run.core.Integration.ProcessDataBase.read_log')
    @patch('Run.core.Integration.ProcessDataBase.log_to_sql')
    @patch('Run.core.Integration.ProcessDataBase.predict_steps')
    @patch('Run.core.Integration.ProcessDataBase.Calculator')
    def test_process_db_successful(self, mock_calc, mock_predict, mock_log_to_sql, mock_read_log):
        # 模拟正常流程
        mock_read_log.return_value = ('mock_log', '2025-06-23')
        mock_calc_instance = MagicMock()
        mock_calc.return_value = mock_calc_instance

        # 不应抛出异常
        process_db('dummy_log.txt')


if __name__ == '__main__':
    unittest.main()
