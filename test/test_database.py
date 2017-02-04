import unittest
import os
from datetime import datetime
from contextlib import closing

os.sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "../src")))

from time_database import TimeDatabase
from utils import *

test_db_name = './test.db'


class TestDatabase(unittest.TestCase):
    @classmethod
    def get_date_time_now(cls):
        return datetime.now().strftime('%Y-%m-%d %H:%M')

    @classmethod
    def get_date_time(cls, year, month, day, hour, minute):
        return '{}-{}-{} {}:{}'.format(year, month, day, hour, minute)

    @classmethod
    def setUpClass(cls):
        cls.log = Logger()
        cls.create_db()
        cls.insert_started_work()

    @classmethod
    def tearDownClass(cls):
        os.remove(test_db_name)

    @classmethod
    def create_db(cls):
        cls.log = Logger()
        with closing(TimeDatabase(test_db_name, cls.log)) as db:
            db.create_tables()

    @classmethod
    def insert_started_work(cls):
        cls.name_one = 'Foo'
        with closing(TimeDatabase(test_db_name, cls.log)) as db:
            db.insert_started_activity(cls.name_one, TimeStamp())

    def test_creation(self):
        expected_tables = ('work_times')
        sql_cmd = 'select name from sqlite_master WHERE TYPE =\'table\''
        self.db = TimeDatabase(test_db_name, self.log)
        cursor = self.db.connection.cursor()
        tables = []
        for table in cursor.execute(sql_cmd):
            tables.append(table[0])

        for table in tables:
            self.assertTrue(table in expected_tables)

    def test_insert_started_work(self):
        sql_cmd = 'select name from work_times'
        self.db = TimeDatabase(test_db_name, self.log)
        cursor = self.db.connection.cursor()
        cursor.execute(sql_cmd)
        row = cursor.fetchone()
        self.assertEqual(row[0], self.name_one)

    def test_insert_finished_work(self):
        name = 'klaus'
        start = TimeStamp(user_string="10.10.2000-12:10")
        end = TimeStamp(user_string="10.10.2000-13:10")

        self.db = TimeDatabase(test_db_name, self.log)
        self.db.insert_started_activity(name, start)
        self.db.insert_finished_activity(name, end)

        sql_cmd = 'select start, end, name, diff from work_times where name = ?'
        cursor = self.db.connection.cursor()
        cursor.execute(sql_cmd, (name,))
        row = cursor.fetchone()

        self.assertEqual(TimeStamp(db_string=row[0]), start)
        self.assertEqual(TimeStamp(db_string=row[1]), end)
        self.assertEqual(row[2], name)
        self.assertEqual(row[3], 1.0)

    def test_start_exists(self):
        name = 'Baz'
        with closing(TimeDatabase(test_db_name, self.log)) as db:
            self.assertFalse(db.start_exists(name))
            db.insert_started_activity(name, TimeStamp())
            self.assertTrue(db.start_exists(name))

    def test_get_activities(self):
        with closing(TimeDatabase(test_db_name, self.log)) as db:
            cursor = db.connection.cursor()
            cursor.execute("delete from work_times",())

        name = "blub"
        s1 = TimeStamp(user_string="10.10.1900-12:00")
        e1 = TimeStamp(user_string="10.10.1900-14:00")
        s2 = TimeStamp(user_string="10.10.2000-12:00")
        e2 = TimeStamp(user_string="10.10.2000-14:00")
        activities = []
        with closing(TimeDatabase(test_db_name, self.log)) as db:
            db.insert_started_activity(name, s1)
            db.insert_finished_activity(name, e1)
            db.insert_started_activity(name, s2)
            db.insert_finished_activity(name, e2)
            activities = db.get_activities(name)
        for activity in activities:
            self.assertEqual(name, activity.name)
            self.assertTrue(activity.start in [s1, s2])
            self.assertTrue(activity.end in [e1, e2])

if __name__ == '__main__':
    unittest.main()
