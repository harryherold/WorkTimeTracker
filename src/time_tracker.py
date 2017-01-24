#!/usr/bin/env python3
import sys
import os.path
import argparse
import operator
from contextlib import closing

from time_database import TimeDatabase
from utils import *
from config import *

# TODO Put this class in separate module
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

    def show_duration_of_activity(self, activity, duration) -> None:
        try:
            [b, e] = [TimeStamp(user_string=t) for t in duration.strip().split(',')]
            requested_interval = TimeInterval(b, e)
        except ValueError:
            self.logger.error('Given time interval has the wrong format')
            return
        with closing(TimeDatabase(self.filename, self.logger, verbose=self.verbose)) as db:
            d = h = m = 0
            (d, h, m) = db.get_duration_of_activity(activity, requested_interval)
            self.logger.print('{:02d}:{:02d}:{:02d}'.format(d,h,m))

def parse_time_string(time_str: str) -> TimeStamp:
    if time_str == 'c':
        return TimeStamp()
    else:
        return TimeStamp(user_string=time_str)

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start", type=str,
                    help="Datetime for starting an activity")

parser.add_argument("-e", "--end", type=str,
                    help="Datetime for ending an activity")

parser.add_argument("-a","--activity", type=str,
                    help="The activity name")

parser.add_argument("-d","--duration", type=str,
                    help="Shows the duration of an interval for a given specific activity.")

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
    tt.show_duration_of_activity(args.activity, args.duration)

if args.start is not None:
    if args.activity is None:
        logger.warning("Activity not given! Can not store start of work time")
        exit(1)
    tt.start_activity(args.activity, parse_time_string(args.start))

if args.end is not None:
    if args.activity is None:
        logger.warning("Activity not given! Can not store end of work time")
        exit(1)
    tt.end_activity(args.activity, parse_time_string(args.end))
