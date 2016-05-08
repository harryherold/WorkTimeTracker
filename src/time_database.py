import sqlite3


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
        """Date has to be in the format %Y-%m-%d %H:%M"""

        insert_cmd = 'insert into work_times (start, name) values (?, ?)'
        cursor = self.connection.cursor()
        cursor.execute(insert_cmd, (date, name))
        self.connection.commit()

    def insert_finished_work(self, name, date):
        """Date has to be in the format %Y-%m-%d %H:%M"""

        update_cmd = 'update work_times set end = ?, ' \
                     'diff = cast(strftime(\'%s\', ?)- strftime(\'%s\',start) as REAL) / 60 / 60 ' \
                     'where end is NULL and name = ?'

        cursor = self.connection.cursor()
        cursor.execute(update_cmd, (date, date, name))
        self.connection.commit()

    def start_exists(self, name):
        """Tests whether a start timestamp exists for an activity"""

        search_cmd = 'select exists(select 1 from work_times where end is NULL and name = ? limit 1)'
        cursor = self.connection.cursor()
        cursor.execute(search_cmd, (name,))
        row = cursor.fetchone()

        return True if row[0] == 1 else False