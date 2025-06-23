import unittest
import os
from Run.core.ConvertData import ReadLogs


class TestReadLogs(unittest.TestCase):

    def setUp(self):
        # 使用符合 read_log 要求的日志文件名：前8位为 YYYYMMDD
        self.sample_log_path = '20240621_test.log'
        with open(self.sample_log_path, 'w') as f:
            f.write("20240621 12:00:00.000 DATA:PZDA WESTVEST_LSA<AA><BB><CC>\n")
            f.write("20240621 12:01:00.000 DATA:PZDA W666<AA><BB><CC>\n")  # 应被排除
            f.write("20240621 12:02:00.000 DATA:PZDA W123<AA><BB><CC>\n")  # 应被识别

    def tearDown(self):
        # 删除测试日志文件
        if os.path.exists(self.sample_log_path):
            os.remove(self.sample_log_path)

    def test_read_log_returns_dict_and_date(self):
        log_data, date = ReadLogs.read_log(self.sample_log_path)

        # 类型校验
        self.assertIsInstance(log_data, dict)
        self.assertIsInstance(date, str)

        # 日期识别正确
        self.assertEqual(date, '2024-06-21')

        # WESTVEST_LSA 应映射为 LSA_689
        self.assertIn('LSA_689', log_data)

        # W666 在排除列表中，应该不被包含
        self.assertNotIn('W666', log_data)

        # W123 应被识别
        self.assertIn('W123', log_data)


if __name__ == '__main__':
    unittest.main()
