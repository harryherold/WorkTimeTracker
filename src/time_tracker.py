import os.path
from time_database import TimeDatabase
db_path = '../work_times.db'


class WorkTime:
    def __init__(self, filename):
        self.filename = filename
        database_exists = os.path.exists(filename)
        self.database = TimeDatabase(self.filename)

        if not database_exists:
            self.database.create_tables()
            print("Database created\n")
        print("Load database {}".format(self.filename))
        self.database.close()


def main():
    wt = WorkTime(db_path)


main()
