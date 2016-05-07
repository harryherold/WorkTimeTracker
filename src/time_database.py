import sqlite3


class TimeDatabase:
    def __init__(self, filename):
        super(TimeDatabase, self).__init__()
        self.filename = filename
        self.connection = sqlite3.connect(self.filename)

    def close(self):
        self.connection.close()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE started_work (id integer,     \
                                                   start DATETIME, \
                                                   name text,      \
                                                   primary key(id))')

        cursor.execute('CREATE TABLE finished_work (id integer,       \
                                                      start DATETIME, \
                                                      end DATETIME,   \
                                                      name text,      \
                                                      diff integer,   \
                                                      primary key(id))')
        self.connection.commit()
        
    def insert_started_work(self, name, date):
        """date has to be in the format %Y-%m-%d %H:%M"""

        insert_cmd = 'insert into started_work (start, name) values (?, ?)'
        cursor = self.connection.cursor()
        cursor.execute(insert_cmd, (date, name))
        self.connection.commit()

    def insert_finished_work(self, name, date):
        pass

    def start_exists(self, name):
        search_cmd = 'select exists(select 1 from started_work where name = ? limit 1)'
        cursor = self.connection.cursor()
        cursor.execute(search_cmd, (name,))
        row = cursor.fetchone()

        return True if row[0] == 1 else False
