import unittest
from k_time_kit.duration import Duration

class TestDuration(unittest.TestCase):
    def test_duration_addition(self):
        dur1 = Duration(sec=30, min=2, hour=3, day=4, year=2)
        dur2 = Duration(sec=20, min=5, hour=1, day=2, year=1)
        result = dur1 + dur2
        self.assertEqual(str(result), "3.0y 6.0d 4.0h 7.0m 50.0s")

    def test_duration_subtraction(self):
        dur1 = Duration(sec=30, min=2, hour=3, day=4, year=2)
        dur2 = Duration(sec=20, min=5, hour=1, day=2, year=1)
        result = dur1 - dur2
        self.assertEqual(str(result), "1.0y 2.0d 1.0h 57.0m 10.0s")

    def test_duration_comparison(self):
        dur1 = Duration(sec=30, min=2, hour=3, day=4, year=2)
        dur2 = Duration(sec=20, min=5, hour=1, day=2, year=1)
        self.assertTrue(dur1 > dur2)

if __name__ == '__main__':
    print("")
    unittest.main()