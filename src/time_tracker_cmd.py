#!/usr/bin/env python3
import sys
import argparse
from utils import *
from config import *
import time_tracker

def parse_time_string(time_str: str) -> TimeStamp:
    if time_str == 'c':
        return TimeStamp()
    else:
        return TimeStamp(user_string=time_str)

if __name__ == "__main__":
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
    tt = time_tracker.TimeTracker(db_path, logger, verbose=args.verbose)

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
