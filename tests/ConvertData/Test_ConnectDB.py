import unittest
import os
from sqlalchemy.engine import Engine, Connection
from Run.core.ConvertData import ConnectDB


class TestConnectDB(unittest.TestCase):

    def setUp(self):
        # 每个测试运行前设置 rootPath
        ConnectDB.rootPath = os.path.abspath(os.path.dirname(__file__))

    def test_sql_engine_disk_mock(self):
        db_name = 'test_db'
        test_path = 'test'
        engine = ConnectDB.sql_engine(db_name, test_path)
        self.assertIsInstance(engine, Engine)

        expected_path = os.path.join(ConnectDB.rootPath, 'DataBase', test_path, f'{db_name}.db')
        self.assertIn(expected_path.replace('\\', '/'), str(engine.url))

    def test_conn_engine_mock(self):
        # 临时 mock sql_engine 并在测试结束后恢复
        engine = ConnectDB.create_engine('sqlite:///:memory:')
        original_sql_engine = ConnectDB.sql_engine
        ConnectDB.sql_engine = lambda *_: engine

        try:
            conn = ConnectDB.conn_engine('mock_db')
            self.assertIsInstance(conn, Connection)
            conn.close()
        finally:
            ConnectDB.sql_engine = original_sql_engine  # 恢复

    def test_create_engine_direct(self):
        engine = ConnectDB.create_engine('sqlite:///:memory:')
        self.assertIsInstance(engine, Engine)


if __name__ == '__main__':
    unittest.main()
