#!/usr/bin/env python3
import sys
import os.path
import argparse

from time_database import TimeDatabase
from utils import *
from config import *


class TimeTracker:
    def __init__(self, filename: str, verbose=False):
        self.verbose = verbose
        self.filename = filename
        database_exists = os.path.exists(self.filename)
        self.database = TimeDatabase(self.filename, self.verbose)
        if not database_exists:
            self.database.create_tables()
            print_info("Database created\n", self.verbose)
        print_info("Connected to database {}".format(self.filename), self.verbose)

    def __del__(self):
        # TODO database.close in destructor is a bad idea -> throws an exception
        self.database.close()

    def start_activity(self, name: str, t: TimeStamp) -> None:
        if self.database.start_exists(name):
            print_warning("This activity is already started")
            return
        self.database.insert_started_work(name, t)

    def end_activity(self, name: str, t: TimeStamp) -> None:
        if not self.database.start_exists(name):
            print_warning("This activity is not started")
            return
        self.database.insert_finished_work(name, t)

    def show_started_work(self) -> None:
        started_work = self.database.get_started_work()
        for e in started_work:
            print("{} => {}".format(e[0], e[1]))

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start", type=str,
                    help="Datetime for starting an activity")

parser.add_argument("-e", "--end", type=str,
                    help="Datetime for ending an activity")

parser.add_argument("-a","--activity", type=str,
                    help="The activity name")

parser.add_argument("--list", action='store_true')

parser.add_argument("-v", "--verbose", action='store_true')

args = parser.parse_args()

tt = TimeTracker(db_path, True if args.verbose is not None else False)

if args.list:
    tt.show_started_work()
    exit(0)

if args.start is not None:
    if args.activity is None:
        print_warning("Activity not given! Can not store start of work time")
        exit(1)
    tt.start_activity(args.activity, TimeStamp(args.start))

if args.end is not None:
    if args.activity is None:
        print_warning("Activity not given! Can not store end of work time")
        exit(1)
    tt.end_activity(args.activity, TimeStamp(args.end))
