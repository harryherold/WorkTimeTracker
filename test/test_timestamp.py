import unittest
import os
from datetime import datetime, timedelta

from devassistant.dapi.dapicli import user

os.sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "../src")))

from utils import TimeStamp

class TestTimeStamp(unittest.TestCase):
    def test_current_date(self):
        current_t = datetime.now()
        t = TimeStamp()
        self.assertEqual(t.day(), current_t.day)
        self.assertEqual(t.month(), current_t.month)
        self.assertEqual(t.year(), current_t.year)

    def test_valid_string(self):
        t = TimeStamp(user_string="5.12.2010-08:00")
        self.assertEqual(t.day(), 5)
        self.assertEqual(t.month(), 12)
        self.assertEqual(t.year(), 2010)
        self.assertEqual(t.hour(), 8)
        self.assertEqual(t.minute(), 0)
        self.assertEqual(str(t), "05.12.2010-08:00")

    def test_invalid_string(self):
        with self.assertRaises(ValueError):
            TimeStamp(user_string="2001-10")
        with self.assertRaises(ValueError):
            TimeStamp(user_string="c-10")

    def test_sub_timestamps(self):
        ts = TimeStamp(user_string="1.12.2010-08:00")
        te = TimeStamp(user_string="2.12.2010-09:01")
        d1 = timedelta(days=1, hours=1, minutes=1)
        self.assertEqual(d1, te - ts)
        te = TimeStamp(user_string="31.12.2010-10:02")
        d1 = timedelta(days=30, hours=2, minutes=2)
        self.assertEqual(d1, te - ts)

if __name__ == '__main__':
    unittest.main()
