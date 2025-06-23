import unittest
import pandas as pd
from Run.core.Analyze import analyze_tool as at  # 确保模块名为 analyze_tool.py，并已正确设置 __init__.py


class TestAnalyzeTool(unittest.TestCase):

    def test_check_werk_voertuig_true(self):
        df = pd.DataFrame({
            '<aanmelden> voertuig': [1001, 1001, 1001],
            '<afmelden> voertuig': [1002, 1003, 1002],
            '<aktuell> voertuig': [1001, 1001, 1001]
        })
        storing = "storing1"
        afdelling = "afd1"
        result = at.check_werk_voertuig(df, storing, afdelling)
        self.assertEqual(result[0], storing)
        self.assertEqual(result[1], afdelling)
        self.assertTrue(result[2])

    def test_check_werk_voertuig_false(self):
        df = pd.DataFrame({
            '<aanmelden> voertuig': [4001, 4001, 4001],
            '<afmelden> voertuig': [4001, 4001, 4001],
            '<aktuell> voertuig': [4001, 4001, 4001]
        })
        storing = "storing3"
        afdelling = "afd3"
        result = at.check_werk_voertuig(df, storing, afdelling)
        self.assertFalse(result[2])

    def test_fifo_fout_detected(self):
        df = pd.DataFrame({
            '<aanmelden> voertuig': [2001, 2002, 2003],
            '<afmelden> voertuig': [2002, 2003, 2004],  # 2001未被 afmelden
            '<aktuell> niveau fifo': [1, 2, 3]
        })
        storing = "storing2"
        afdelling = "afd2"
        result = at.fifo_fout(df, storing, afdelling)
        self.assertEqual(result[0], storing)
        self.assertEqual(result[1], afdelling)
        self.assertTrue(result[-1])  # 错误状态应为 True

    def test_fifo_fout_not_detected(self):
        df = pd.DataFrame({
            '<aanmelden> voertuig': [3001, 3002, 3003],
            '<afmelden> voertuig': [3001, 3002, 3003],
            '<aktuell> niveau fifo': [0, 1, 1]
        })
        storing = "storing4"
        afdelling = "afd4"
        result = at.fifo_fout(df, storing, afdelling)
        self.assertFalse(result[-1])  # 错误状态应为 False


if __name__ == '__main__':
    unittest.main()
