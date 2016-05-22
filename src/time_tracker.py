import os.path
from time_database import TimeDatabase
from datetime import datetime

db_path = '../work_times.db'


class TimeTracker:
    def __init__(self, filename):
        self.filename = filename
        database_exists = os.path.exists(self.filename)
        self.database = TimeDatabase(self.filename)
        if not database_exists:
            self.database.create_tables()
            print("Database created\n")
        print("Load database {}".format(self.filename))

    def __del__(self):
        self.database.close()

    def start_activity(self, name, t=None):
        if t is None:
            t = datetime.now().strftime("%Y-%m-%d %H:%M")
        if self.database.start_exists(name):
            print("This activity is already started")
            return
        self.database.insert_started_work(name, t)

    def end_activity(self, name, t=None):
        if t is None:
            t = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not self.database.start_exists(name):
            print("This activity is not started")
            return
        self.database.insert_finished_work(name, t)


def main():
    tt = TimeTracker(db_path)
    tt.start_activity("Foo")
    tt.end_activity("Foo")


main()
