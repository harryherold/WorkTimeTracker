import unittest
import os
from datetime import datetime

os.sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "../src")))

from time_database import TimeDatabase

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
        cls.create_db()
        cls.insert_started_work()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        os.remove(test_db_name)

    @classmethod
    def create_db(cls):
        cls.db = TimeDatabase(test_db_name)
        cls.db.create_tables()

    @classmethod
    def insert_started_work(cls):
        cls.name_one = 'Foo'
        cls.db.insert_started_work(cls.name_one, cls.get_date_time_now())

    def test_creation(self):
        expected_tables = ('work_times')
        sql_cmd = 'select name from sqlite_master WHERE TYPE =\'table\''
        cursor = self.db.connection.cursor()
        tables = []
        for table in cursor.execute(sql_cmd):
            tables.append(table[0])

        for table in tables:
            self.assertTrue(table in expected_tables)

    def test_insert_started_work(self):
        sql_cmd = 'select name from work_times'
        cursor = self.db.connection.cursor()
        cursor.execute(sql_cmd)
        row = cursor.fetchone()
        self.assertEqual(row[0], self.name_one)

    # def test_insert_finished_work(self):
    #     name = 'klaus'
    #     start = self.get_date_time(2000, 4, 10, 12, 0)
    #     end = self.get_date_time(2000, 4, 10, 13, 0)
    #
    #     self.db.insert_started_work(name, start)
    #     self.db.insert_finished_work(name, end)
    #
    #     sql_cmd = 'select start, end, name, diff from finished_work where name = ?'
    #     cursor = self.db.connection.cursor()
    #     cursor.execute(sql_cmd, (name,))
    #     row = cursor.fetchone()
    #
    #     self.assertEqual(row[0], start)
    #     self.assertEqual(row[1], end)
    #     self.assertEqual(row[2], name)
    #     self.assertEqual(row[3], 1)

    def test_start_exists(self):
        name = 'Baz'
        self.assertFalse(self.db.start_exists(name))
        self.db.insert_started_work(name, self.get_date_time_now())
        self.assertTrue(self.db.start_exists(name))


if __name__ == '__main__':
    unittest.main()
