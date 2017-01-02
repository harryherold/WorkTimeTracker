import unittest
import os
from datetime import datetime

os.sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "../src")))

from utils import TimeStamp, TimeInterval

class TestTimeInterval(unittest.TestCase):
    def test_lesser(self):
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-08:30")
        t3 = TimeStamp("1.12.2010-08:31")
        t4 = TimeStamp("1.12.2010-08:32")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertTrue(ti1 < ti2)
        self.assertFalse(ti2 < ti1)
        t5 = TimeStamp("1.12.2009-08:30")
        t6 = TimeStamp("1.12.2009-08:31")
        ti3 = TimeInterval(t5, t6)
        self.assertTrue(ti3 < ti2)
        self.assertFalse(ti2 < ti3)

    def test_lesser_equal(self):
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-10:00")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertTrue(ti1 <= ti2)
        self.assertFalse(ti2 <= ti1)
        t5 = TimeStamp("1.12.2010-09:30")
        t6 = TimeStamp("1.12.2010-10:00")
        ti3 = TimeInterval(t5, t6)
        self.assertTrue(ti2 <= ti3)
        self.assertFalse(ti3 <= ti2)

    def test_disjunct(self):
        # Case 0: Intervals are overlapped
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-10:00")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertFalse(ti1.disjunct(ti2))
        self.assertFalse(ti2.disjunct(ti1))
        # Case 1: One interval contains the other
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-09:20")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertFalse(ti1.disjunct(ti2))
        self.assertFalse(ti2.disjunct(ti1))
        # Case 2: Intervals are disjunct
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:31")
        t4 = TimeStamp("1.12.2010-09:40")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertTrue(ti1.disjunct(ti2))
        self.assertTrue(ti2.disjunct(ti1))

    def test_contains(self):
        # Case 0: Intervals are overlapped
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-10:00")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertFalse(ti1.contains(ti2))
        self.assertFalse(ti2.contains(ti1))
        # Case 1: One interval contains the other
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-09:20")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertTrue(ti1.contains(ti2))
        self.assertFalse(ti2.contains(ti1))
        # Case 2: Intervals are disjunct
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:31")
        t4 = TimeStamp("1.12.2010-09:40")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertFalse(ti1.contains(ti2))
        self.assertFalse(ti2.contains(ti1))

    def test_overlapps(self):
        # Case 0: Intervals are overlapped
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-10:00")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertTrue(ti1.overlapps(ti2))
        self.assertTrue(ti2.overlapps(ti1))
        # Case 1: One interval contains the other
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-09:20")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertFalse(ti1.overlapps(ti2))
        self.assertFalse(ti2.overlapps(ti1))
        # Case 2: Intervals are disjunct
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:31")
        t4 = TimeStamp("1.12.2010-09:40")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertFalse(ti1.overlapps(ti2))
        self.assertFalse(ti2.overlapps(ti1))

    def test_intersection(self):
        # Case 0: Intervals are overlapped
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-10:00")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertEqual(ti1.intersection(ti2), (0, 0, 15))
        self.assertEqual(ti2.intersection(ti1), (0, 0, 15))
        # Case 1: One interval contains the other
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:15")
        t4 = TimeStamp("1.12.2010-09:20")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertEqual(ti1.intersection(ti2), (0, 0, 5))
        self.assertEqual(ti2.intersection(ti1), (0, 0, 5))
        # Case 2: Intervals are disjunct
        t1 = TimeStamp("1.12.2010-08:00")
        t2 = TimeStamp("1.12.2010-09:30")
        t3 = TimeStamp("1.12.2010-09:31")
        t4 = TimeStamp("1.12.2010-09:40")
        ti1 = TimeInterval(t1, t2)
        ti2 = TimeInterval(t3, t4)
        self.assertEqual(ti1.intersection(ti2), (0, 0, 0))
        self.assertEqual(ti2.intersection(ti1), (0, 0, 0))

if __name__ == '__main__':
    unittest.main()
