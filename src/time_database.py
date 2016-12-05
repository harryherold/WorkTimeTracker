import sqlite3
from typing import List
from utils import *


class TimeDatabase:
    def __init__(self, filename: str, log: Logger, verbose=False):
        """Connects to the database"""
        self.log = log
        self.verbose = verbose
        self.filename = filename
        self.connection = sqlite3.connect(self.filename)

    def close(self) -> None:
        """Disconnect the database"""
        self.connection.close()

    def create_tables(self) -> None:
        """Creates database and tables"""

        cursor = self.connection.cursor()
        # TODO Throws an execption
        cursor.execute('CREATE TABLE work_times (id integer,       \
                                                 start DATETIME, \
                                                 end DATETIME,   \
                                                 name text,      \
                                                 diff real,   \
                                                 primary key(id))')
        self.connection.commit()

    def insert_started_work(self, name: str, date: TimeStamp) -> None:

        insert_cmd = 'insert into work_times (start, name) values (?, ?)'
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_cmd, (str(date), name))
            self.connection.commit()
        except sqlite3.Error as err:
            self.log.error("Cannot store starting time in database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Stored in database", self.verbose)

    def insert_finished_work(self, name: str, date: TimeStamp) -> None:

        update_cmd = 'update work_times set end = ?, ' \
                     'diff = cast(strftime(\'%s\', ?)- strftime(\'%s\',start) as REAL) / 60 / 60 ' \
                     'where end is NULL and name = ?'
        cursor = self.connection.cursor()
        try:
            cursor.execute(update_cmd, (str(date), str(date), name))
            self.connection.commit()
        except sqlite3.Error as err:
            self.log.error("Cannot store ending time in database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Stored in database", self.verbose)

    def get_started_activities(self) -> List[str]:
        """Returns a structure that includes all started activities with time"""

        search_cmd = 'select start, name from work_times where end is NULL'
        cursor = self.connection.cursor()
        try:
            cursor.execute(search_cmd)
        except sqlite3.Error as err:
            self.log.error("Cannot select started activities in database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Selected entries in database")

        rows = cursor.fetchall()
        started_work = [row[1] for row in rows]
        return started_work

    def start_exists(self, name: str) -> bool:
        """Tests whether a start timestamp exists for an activity"""

        search_cmd = 'select exists(select 1 from work_times where end is NULL and name = ? limit 1)'
        cursor = self.connection.cursor()
        cursor.execute(search_cmd, (name,))
        row = cursor.fetchone()

        return True if row[0] == 1 else False
