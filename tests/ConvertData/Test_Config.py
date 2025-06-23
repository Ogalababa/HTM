import unittest
import sys
import os

from sqlalchemy.testing.config import Config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from Run.core.ConvertData.Config import WisselData  # 修改为Config.py中实际类名


class TestWisselData(unittest.TestCase):

    def setUp(self):
        self.hex_data = "2025-06-23 12:00:00 WESTVEST_LSA PZDA<1A><2B><3C>"
        self.bit_config = {"LSA_689": {"bit1": 1}}
        self.byte_config = {"LSA_689": {"byte1": (0, 4)}}
        self.wissel = WisselData(self.hex_data, self.bit_config, self.byte_config)

    def test_init(self):
        self.assertIn("server time", self.wissel.wissel_info)
        self.assertIn("wissel nr", self.wissel.wissel_info)

    def test_line_to_hex(self):
        result = self.wissel.line_to_hex()
        self.assertIn("1A", result)
        self.assertIn("2B", result)
        self.assertIn("3C", result)

    def test_list_to_str(self):
        self.wissel.hex_str_list = ["1A", "2B", "3C"]
        result = self.wissel.list_to_str()
        self.assertEqual(result, "3C2B1A")

    def test_hex_to_bin(self):
        self.wissel.hex_str = "1F"
        result = self.wissel.hex_to_bin()
        self.assertEqual(result, "00011111")

    def test_covert_data(self):
        self.wissel.bin_data = "0000100000000001000000000000000011111111" + "0" * 8
        self.wissel.single_bit = {"bit1": 2}
        self.wissel.multi_bits = {"byte1": (0, 4)}
        result = self.wissel.covert_data()
        self.assertIn("Count", result)
        self.assertIn("date-time", result)
        self.assertIn("byte1", result)
        self.assertIn("bit1", result)

    def test_wissel_version(self):
        self.wissel.wissel_version("LSA_689")
        self.assertEqual(self.wissel.single_bit, self.bit_config["LSA_689"])
        self.assertEqual(self.wissel.multi_bits, self.byte_config["LSA_689"])


if __name__ == '__main__':
    unittest.main()