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
            db.insert_started_work(cls.name_one, cls.get_date_time_now())

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
        start = self.get_date_time(2000, 10, 10, 12, 10)
        end = self.get_date_time(2000, 10, 10, 13, 10)

        self.db = TimeDatabase(test_db_name, self.log)
        self.db.insert_started_work(name, start)
        self.db.insert_finished_work(name, end)

        sql_cmd = 'select start, end, name, diff from work_times where name = ?'
        cursor = self.db.connection.cursor()
        cursor.execute(sql_cmd, (name,))
        row = cursor.fetchone()

        self.assertEqual(row[0], start)
        self.assertEqual(row[1], end)
        self.assertEqual(row[2], name)
        self.assertEqual(row[3], 1.0)

    def test_start_exists(self):
        name = 'Baz'
        with closing(TimeDatabase(test_db_name, self.log)) as db:
            self.assertFalse(db.start_exists(name))
            db.insert_started_work(name, self.get_date_time_now())
            self.assertTrue(db.start_exists(name))


if __name__ == '__main__':
    unittest.main()
