import os.path
import datetime
from contextlib import closing

from time_database import TimeDatabase
from utils import Activity,TimeStamp,Logger,TimeInterval

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
            activities = db.get_activities_from_interval(activity, requested_interval)
            d = datetime.timedelta(days=0, seconds=0)
            for activity in activities:
                start = activity.start
                end = TimeStamp() if not activity.end else activity.end
                d += TimeInterval(start, end).intersection(requested_interval)
            hours = int(d.seconds / 3600)
            minutes = int((d.seconds - (hours * 3600)) / 60)
            self.logger.print('{:02d}:{:02d}:{:02d}'.format(d.days, hours, minutes))

    def show_all_activities(self, activity=None):
        with closing(TimeDatabase(self.filename, self.logger, verbose=self.verbose)) as db:
            activities = db.get_activities()
            for activity in activities:
                self.logger.print(activity)
