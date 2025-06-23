import unittest
import os
from sqlalchemy.engine import Engine, Connection
from Run.core.ConvertData import ConnectDB


class TestConnectDB(unittest.TestCase):

    def setUp(self):
         
        ConnectDB.rootPath = os.path.abspath(os.path.dirname(__file__))

    def test_conn_engine_mock(self):
         
        engine = ConnectDB.create_engine('sqlite:///:memory:')
        original_sql_engine = ConnectDB.sql_engine
        ConnectDB.sql_engine = lambda *_: engine

        try:
            conn = ConnectDB.conn_engine('mock_db')
            self.assertIsInstance(conn, Connection)
            conn.close()
        finally:
            ConnectDB.sql_engine = original_sql_engine   

    def test_create_engine_direct(self):
        engine = ConnectDB.create_engine('sqlite:///:memory:')
        self.assertIsInstance(engine, Engine)


if __name__ == '__main__':
    unittest.main()
