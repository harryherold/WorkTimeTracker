#!/bin/python3

import sys
import os.path
import argparse
from time_database import TimeDatabase
from datetime import datetime
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


def convert_datetime(t):
    return datetime.strptime(t, "%d.%m.%Y-%H:%M")


def is_datetime(t):
    try:
        convert_datetime(t)
    except ValueError:
        return False
    return True


def get_time_stamp(date_time_str):
    t = None
    if is_datetime(date_time_str):
        t = convert_datetime(date_time_str)
    return t

tt = TimeTracker(db_path)

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start", type=str,
                    help="Datetime for starting an activity")

parser.add_argument("-e", "--end", type=str,
                    help="Datetime for ending an activity")

parser.add_argument("activity", type=str,
                    help="The activity name")

args = parser.parse_args()

if args.start is not None:
    ts = get_time_stamp(args.start)
    tt.start_activity(args.activity, ts)

if args.end is not None:
    te = get_time_stamp(args.end)
    tt.end_activity(args.activity, te)
