import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Run.core.ConvertData import ImportConf
import Run.conf.conf as conf


class TestImportConf(unittest.TestCase):

    def test_bit_config(self):
        result = ImportConf.bit_config()
        self.assertEqual(result, conf.bit_configs)
        self.assertIsInstance(result, dict)

    def test_byte_config(self):
        result = ImportConf.byte_config()
        self.assertEqual(result, conf.byte_configs)
        self.assertIsInstance(result, dict)

    def test_drop_config(self):
        result = ImportConf.drop_config()
        self.assertEqual(result, conf.drop_configs)
        self.assertIsInstance(result, dict)  # ✅ 修复这里


if __name__ == '__main__':
    unittest.main()
