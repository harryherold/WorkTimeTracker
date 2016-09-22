import sqlite3

from utils import TimeStamp

class TimeDatabase:
    def __init__(self, filename):
        """Connects to the database"""
        self.filename = filename
        self.connection = sqlite3.connect(self.filename)

    def close(self):
        """Disconnect the database"""
        self.connection.close()

    def create_tables(self):
        """Creates database and tables"""

        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE work_times (id integer,       \
                                                 start DATETIME, \
                                                 end DATETIME,   \
                                                 name text,      \
                                                 diff real,   \
                                                 primary key(id))')
        self.connection.commit()
        
    def insert_started_work(self, name, date):

        insert_cmd = 'insert into work_times (start, name) values (?, ?)'
        cursor = self.connection.cursor()
        try:
            cursor.execute(insert_cmd, (str(date), name))
            self.connection.commit()
        except sqlite3.Error as err:
            print("Cannot store starting time in database")
            print("Error:\n{}".format(err.args[0]))
        else:
            print("Stored in database")

    def insert_finished_work(self, name, date):

        update_cmd = 'update work_times set end = ?, ' \
                     'diff = cast(strftime(\'%s\', ?)- strftime(\'%s\',start) as REAL) / 60 / 60 ' \
                     'where end is NULL and name = ?'
        cursor = self.connection.cursor()
        try:
            cursor.execute(update_cmd, (str(date), str(date), name))
            self.connection.commit()
        except sqlite3.Error as err:
            print("Cannot store ending time in database")
            print("Error:\n{}".format(err.args[0]))
        else:
            print("Stored in database")

    def get_started_work(self):
        """Returns a structure that includes all started activities with time"""

        search_cmd = 'select start, name from work_times where end is NULL'
        cursor = self.connection.cursor()
        cursor.execute(search_cmd)
        rows = cursor.fetchall()
        started_work = []
        for row in rows:
            started_work.append([row[0], row[1]])
        return started_work

    def start_exists(self, name):
        """Tests whether a start timestamp exists for an activity"""

        search_cmd = 'select exists(select 1 from work_times where end is NULL and name = ? limit 1)'
        cursor = self.connection.cursor()
        cursor.execute(search_cmd, (name,))
        row = cursor.fetchone()

        return True if row[0] == 1 else False