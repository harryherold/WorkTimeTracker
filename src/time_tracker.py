#!/bin/python3

import os.path
import argparse
from time_database import TimeDatabase
from utils import TimeStamp
db_path = '/home/cherold/Documents/work_times.db'


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

    def start_activity(self, name, t):
        if self.database.start_exists(name):
            print("This activity is already started")
            return
        self.database.insert_started_work(name, t)

    def end_activity(self, name, t):
        if not self.database.start_exists(name):
            print("This activity is not started")
            return
        self.database.insert_finished_work(name, t)

    def show_started_work(self):
        started_work = self.database.get_started_work()
        for e in started_work:
            print("{} => {}".format(e[0], e[1]))

tt = TimeTracker(db_path)

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start", type=str,
                    help="Datetime for starting an activity")

parser.add_argument("-e", "--end", type=str,
                    help="Datetime for ending an activity")

# TODO Only important with start or end argument
parser.add_argument("activity", type=str,
                    help="The activity name")

parser.add_argument("--list", action='store_true')

args = parser.parse_args()

if args.start is not None:
    tt.start_activity(args.activity, TimeStamp(args.start))

if args.end is not None:
    tt.end_activity(args.activity, TimeStamp(args.end))
