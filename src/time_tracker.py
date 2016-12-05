#!/usr/bin/env python3
import sys
import os.path
import argparse
from contextlib import closing

from time_database import TimeDatabase
from utils import *
from config import *


class TimeTracker:
    def __init__(self, filename: str, logger: Logger, verbose=False):
        self.logger = logger
        self.verbose = verbose
        self.filename = filename
        database_exists = os.path.exists(self.filename)
        if not database_exists:
            with closing(TimeDatabase(self.filename, self.logger, verbose=self.verbose)) as db:
                db.create_tables()
                self.logger.info("Database created\n", self.verbose)
        self.logger.info("Connected to database {}".format(self.filename), self.verbose)

    def start_activity(self, name: str, t: TimeStamp) -> None:
        with closing(TimeDatabase(self.filename, self.logger, verbose=self.verbose)) as db:
            if db.start_exists(name):
                self.logger.warning("This activity is already started")
                return
            db.insert_started_work(name, t)

    def end_activity(self, name: str, t: TimeStamp) -> None:
        with closing(TimeDatabase(self.filename, self.logger, verbose=self.verbose)) as db:
            if not db.start_exists(name):
                self.logger.warning("This activity is not started")
                return
            db.insert_finished_work(name, t)

    def show_started_work(self) -> None:
        with closing(TimeDatabase(self.filename, self.logger, verbose=self.verbose)) as db:
            started_work = db.get_started_activities()
            if started_work:
                self.logger.print(','.join(started_work))
            else:
                self.logger.print('No activity')

    def show_duration_of_activity(self, activity) -> None:
        with closing(TimeDatabase(self.filename, self.logger, verbose=self.verbose)) as db:
            if not db.start_exists(activity):
                self.logger.warning("This activity is not started")
                return
            # TODO Add subtraction of timestamps and printing its difference
            print(db.get_time_of_started_activity(activity))


parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start", type=str,
                    help="Datetime for starting an activity")

parser.add_argument("-e", "--end", type=str,
                    help="Datetime for ending an activity")

parser.add_argument("-a","--activity", type=str,
                    help="The activity name")

parser.add_argument("-d","--duration", action='store_true',
                    help="Shows all started activities.")

parser.add_argument("--logfile", type=str,
                    help="Specifies a log file for the output."
                         "If the file does not exists, it will be created")

parser.add_argument("--list", action='store_true',
                    help="Shows all started activities.")

parser.add_argument("-v", "--verbose", action='store_true')

args = parser.parse_args()

logger = Logger(args.logfile)
tt = TimeTracker(db_path, logger, verbose=args.verbose)

if args.list:
    tt.show_started_work()
    exit(0)

if args.duration:
    if args.activity is None:
        logger.warning("Activity not given to show the current duration!")
        exit(1)
    tt.show_duration_of_activity(args.activity)

if args.start is not None:
    if args.activity is None:
        logger.warning("Activity not given! Can not store start of work time")
        exit(1)
    tt.start_activity(args.activity, TimeStamp(args.start))

if args.end is not None:
    if args.activity is None:
        logger.warning("Activity not given! Can not store end of work time")
        exit(1)
    tt.end_activity(args.activity, TimeStamp(args.end))
