import unittest
import os
from Run.core.ConvertData import ReadLogs


class TestReadLogs(unittest.TestCase):

    def setUp(self):
         
        self.sample_log_path = '20240621_test.log'
        with open(self.sample_log_path, 'w') as f:
            f.write("20240621 12:00:00.000 DATA:PZDA WESTVEST_LSA<AA><BB><CC>\n")
            f.write("20240621 12:01:00.000 DATA:PZDA W666<AA><BB><CC>\n")   
            f.write("20240621 12:02:00.000 DATA:PZDA W123<AA><BB><CC>\n")   

    def tearDown(self):
         
        if os.path.exists(self.sample_log_path):
            os.remove(self.sample_log_path)

    def test_read_log_returns_dict_and_date(self):
        log_data, date = ReadLogs.read_log(self.sample_log_path)

         
        self.assertIsInstance(log_data, dict)
        self.assertIsInstance(date, str)

         
        self.assertEqual(date, '2024-06-21')

         
        self.assertIn('LSA_689', log_data)

         
        self.assertNotIn('W666', log_data)

         
        self.assertIn('W123', log_data)


if __name__ == '__main__':
    unittest.main()
