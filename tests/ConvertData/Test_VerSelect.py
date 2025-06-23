# tests/ConvertData/Test_VerSelect.py

import unittest
from Run.core.ConvertData.VerSelect import get_version, get_wissel_type_nr

class TestVerSelect(unittest.TestCase):

    def test_get_version_with_string(self):
        self.assertEqual(get_version('W050'), 'denAJB1C')
        self.assertEqual(get_version('W662'), 'denBQA5C')
        self.assertEqual(get_version('W540'), 'denhBA04')

    def test_get_version_with_list(self):
        self.assertEqual(get_version(['W050']), 'denAJB1C')
        self.assertEqual(get_version(['W662']), 'denBQA5C')

    def test_get_wissel_type_nr_valid(self):
        self.assertIn('W050', get_wissel_type_nr('denAJB1C'))
        self.assertIn('W540', get_wissel_type_nr('denhBA04'))

    def test_get_wissel_type_nr_invalid(self):
        self.assertIsNone(get_wissel_type_nr('non_existing_type'))

if __name__ == '__main__':
    unittest.main()
