import unittest
import pandas as pd
from Run.core.Analyze.wissel_vrij_list import wissel_cycle_list

class TestWisselCycleList(unittest.TestCase):

    def test_start_index_zero_missing(self):
        # 开头没有 index 0，函数应自动插入
        df = pd.DataFrame({
            '<wissel> vergrendeld': [1, 1, 0, 1, 0]
        })
        result = wissel_cycle_list(df)
        self.assertEqual(result[0], 0)

    def test_all_locked(self):
        # 所有都为锁定状态，返回应只含 index 0
        df = pd.DataFrame({
            '<wissel> vergrendeld': [1, 1, 1, 1]
        })
        result = wissel_cycle_list(df)
        self.assertEqual(result, [0])


if __name__ == '__main__':
    unittest.main()
