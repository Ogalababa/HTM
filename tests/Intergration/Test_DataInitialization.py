import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os

from Run.core.Integration import DataInitialization


class TestDataInitialization(unittest.TestCase):

    @patch('Run.core.Integration.DataInitialization.conn_engine')
    @patch('sqlalchemy.inspect')
    @patch('pandas.read_sql_table')
    def test_get_alldata_from_db(self, mock_read_sql, mock_inspect, mock_engine):
        mock_engine.return_value = MagicMock()
        mock_insp = MagicMock()
        mock_insp.get_table_names.return_value = ['table1', 'table2']
        mock_inspect.return_value = mock_insp
        mock_read_sql.side_effect = [
            pd.DataFrame({'a': [1]}),
            pd.DataFrame({'b': [2]})
        ]
        result = DataInitialization.get_alldata_from_db('test_db', path='mock_dir')
        self.assertIn('table1', result)
        self.assertIn('table2', result)
        self.assertTrue(isinstance(result['table1'], pd.DataFrame))

    @patch('Run.core.Integration.DataInitialization.conn_engine')
    def test_save_to_sql_single_table(self, mock_engine):
        mock_df = pd.DataFrame({'col1': [1, 2]})
        data_dict = {'test_table': mock_df}
        mock_conn = MagicMock()
        mock_engine.return_value = mock_conn
        with patch.object(mock_df, 'to_sql') as mock_to_sql:
            DataInitialization.save_to_sql('test_db', data_dict, path='mock_dir')
            mock_to_sql.assert_called_once_with('test_table', mock_conn, index=False, if_exists='replace')

    @patch('Run.core.Integration.DataInitialization.conn_engine')
    def test_save_to_sql_multiple_tables(self, mock_engine):
        df1 = pd.DataFrame({'x': [1]})
        df2 = pd.DataFrame({'y': [2]})
        data_dict = {'table1': df1, 'table2': df2}
        mock_conn = MagicMock()
        mock_engine.return_value = mock_conn

        with patch.object(df1, 'to_sql') as mock_to_sql1, \
             patch.object(df2, 'to_sql') as mock_to_sql2:
            DataInitialization.save_to_sql('test_db', data_dict, path='mock_dir')
            mock_to_sql1.assert_called_once()
            mock_to_sql2.assert_called_once()


if __name__ == '__main__':
    unittest.main()
