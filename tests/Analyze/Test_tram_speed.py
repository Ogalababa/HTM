import unittest
import pandas as pd
from datetime import datetime, timedelta
from Run.core.Analyze.tram_speed import calculation_tram_speed

class TestCalculationTramSpeed(unittest.TestCase):

    def setUp(self):
        # 创建一个合理结构的测试 DataFrame
        base_time = datetime(2024, 1, 1, 12, 0, 0)
        self.dataset = pd.DataFrame({
            'date-time': [base_time, base_time + timedelta(seconds=1), base_time + timedelta(seconds=2),
                          base_time + timedelta(seconds=3), base_time + timedelta(seconds=4)],
            '<afmelden> voertuig': [4001, 4001, 4001, 4001, 4001],
            '<hfk> aanwezigheidslus bezet': [0, 1, 1, 1, 0],
            'Count': [10, 11, 12, 13, 14],
            '<wissel> links': [0, 0, 1, 0, 0],
            '<wissel> rechts': [0, 0, 0, 0, 0],
            'wissel nr': [101, 101, 101, 101, 101],
            '<aanmelden> voertuig': [4001, 4001, 4001, 4001, 4001],
            '<aanmelden> lijn': ['2', '2', '2', '2', '2'],
            '<aanmelden> service': ['D', 'D', 'D', 'D', 'D'],
            '<aanmelden> categorie': ['A', 'A', 'A', 'A', 'A'],
        })

    def test_speed_calculation_valid_data(self):
        result = calculation_tram_speed(self.dataset)
        self.assertEqual(len(result), 1)
        self.assertIn('snelheid km/h', result[0].columns)
        self.assertTrue(0 < result[0]['snelheid km/h'][0] < 50)

    def test_speed_calculation_invalid_voertuig(self):
        # 使用无效车辆编号测试（超出条件）
        df_invalid = self.dataset.copy()
        df_invalid['<afmelden> voertuig'] = [9999] * 5
        result = calculation_tram_speed(df_invalid)
        self.assertEqual(result, [])

    def test_speed_too_high_should_be_filtered(self):
        # hfk_in 和 hfk_out 间隔极短导致速度超标
        df = self.dataset.copy()
        df['date-time'] = [datetime(2024, 1, 1, 12, 0, 0) + timedelta(milliseconds=i) for i in range(5)]
        result = calculation_tram_speed(df)
        self.assertEqual(result, [])  # 应该被过滤掉

    def test_not_enough_data_points(self):
        df = self.dataset.iloc[:2].copy()
        result = calculation_tram_speed(df)
        self.assertEqual(result, [])  # 少于3个点

    def test_bad_contact_should_filter_out(self):
        df = self.dataset.copy()
        df.loc[1, '<hfk> aanwezigheidslus bezet'] = 0  # 模拟数据断裂
        result = calculation_tram_speed(df)
        self.assertEqual(result, [])  # 应被排除

if __name__ == '__main__':
    unittest.main()
