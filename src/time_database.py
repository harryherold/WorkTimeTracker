import sqlite3
from typing import List
from utils import *
import operator
import datetime

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
        try:
            cursor.execute('CREATE TABLE work_times (id integer,     \
                                                     start DATETIME, \
                                                     end DATETIME,   \
                                                     name text,      \
                                                     diff real,      \
                                                     primary key(id))')
            self.connection.commit()
        except sqlite3.Error as err:
            self.log.error("Cannot create database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Created database", self.verbose)

    def insert_started_work(self, name: str, date: TimeStamp) -> None:
        """Stores the starting of an activity"""

        insert_cmd = 'insert into work_times (start, name) values (?, ?)'
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_cmd, (date.db_string(), name))
            self.connection.commit()
        except sqlite3.Error as err:
            self.log.error("Cannot store starting time in database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Stored in database", self.verbose)

    def insert_finished_work(self, name: str, date: TimeStamp) -> None:
        """Stores the timestamp of the end of the activity"""
        """This requires that the activity was started before"""

        update_cmd = 'update work_times set end = ?, ' \
                     'diff = cast(strftime(\'%s\', ?)- strftime(\'%s\',start) as REAL) / 60 / 60 ' \
                     'where end is NULL and name = ?'
        cursor = self.connection.cursor()
        try:
            cursor.execute(update_cmd, (date.db_string(), date.db_string(), name))
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
            self.log.info("Selected entries in database", self.verbose)
        rows = cursor.fetchall()
        started_work = [row[1] for row in rows]
        return started_work

    # TODO rename method, the name is misleading
    def start_exists(self, name: str) -> bool:
        """Tests whether a start timestamp exists for an activity and no end timestamp"""

        select_cmd = 'select exists(select 1 from work_times where end is NULL and name = ? limit 1)'
        cursor = self.connection.cursor()
        cursor.execute(select_cmd, (name,))
        row = cursor.fetchone()
        return True if row[0] == 1 else False

	# TODO test case is missing
    def get_start_time_of_activity(self, name: str) -> TimeStamp:
        """Returns the timestamp of given and started activity"""

        select_cmd = 'select start from work_times where end is NULL and name = ? limit 1'
        cursor = self.connection.cursor()
        try:
            cursor.execute(select_cmd, (name,))
        except sqlite3.Error as err:
            self.log.error("Cannot select time of started activities in database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Selected time of started activity in database", self.verbose)
        row = cursor.fetchone()
        return TimeStamp(db_string=row[0])

	# TODO test case is missing
    def get_duration_of_activity(self, name: str, interval: TimeInterval):
        """Returns the duration that a completed activity took as a tuple of (day, hour, minute)"""

        select_cmd = 'select start, end from work_times where name = ? and \
                      ((start between ? and ?) or (end between ? and ?))'

        cursor = self.connection.cursor()

        try:
            cursor.execute(select_cmd, (name,                       \
                                        interval.begin.db_string(), \
                                        interval.end.db_string(),   \
                                        interval.begin.db_string(), \
                                        interval.end.db_string()))
        except sqlite3.Error as err:
            self.log.error("Cannot select times completed activities in database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Selected times completed activities in database", self.verbose)
        rows = cursor.fetchall()
        duration = datetime.timedelta(days=0, seconds=0)
        for row in rows:
            b = TimeStamp(db_string=row[0])
            e = TimeStamp(db_string=row[1])
            duration += TimeInterval(b, e).intersection(interval)
        return duration
