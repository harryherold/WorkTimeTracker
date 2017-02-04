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
            cursor.execute("CREATE TABLE work_times (id INTEGER,     \
                                                     start DATETIME, \
                                                     end DATETIME,   \
                                                     name TEXT,      \
                                                     diff REAL,      \
                                                     PRIMARY KEY(id))")
            self.connection.commit()
        except sqlite3.Error as err:
            self.log.error("Cannot create database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Created database", self.verbose)

    def insert_started_activity(self, name: str, date: TimeStamp) -> None:
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

    def insert_finished_activity(self, name: str, date: TimeStamp) -> None:
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
    def get_activities_from_interval(self, name: str, interval: TimeInterval):
        """Returns the duration that a completed activity took as a tuple of (day, hour, minute)"""

        select_cmd = 'select name, start, end from work_times where name like ? and \
                      ((start between ? and ?) or (end between ? and ?))'
        cursor = self.connection.cursor()
        try:
            cursor.execute(select_cmd, (name if name else '%', \
                                        interval.begin.db_string(), \
                                        interval.end.db_string(), \
                                        interval.begin.db_string(), \
                                        interval.end.db_string()))
        except sqlite3.Error as err:
            self.log.error("Cannot select times completed activities in database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Selected times completed activities in database", self.verbose)
        rows = cursor.fetchall()
        activities = []
        for row in rows:
            end = None if not row[2] else TimeStamp(db_string=row[2])
            activities.append(Activity(TimeStamp(db_string=row[1]), end, row[0]))
        return activities

    # TODO test case is missing
    def get_activities(self, activity=None):
        select_cmd = 'select name, start, end from work_times where name like ?'
        cursor = self.connection.cursor()
        try:
            cursor.execute(select_cmd, (activity if activity else '%',))
        except sqlite3.Error as err:
            self.log.error("Cannot select times completed activities in database")
            self.log.error("{}".format(err.args[0]))
        else:
            self.log.info("Selected times completed activities in database", self.verbose)
        rows = cursor.fetchall()
        activities = []
        for row in rows:
            end = None if not row[2] else row[2]
            activities.append(Activity(TimeStamp(db_string=row[1]), end, row[0]))
        return activities
