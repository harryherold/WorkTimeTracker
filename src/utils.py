from datetime import datetime
from datetime import timedelta


def always_active(f):
    def _always_active(self, mesg: str, is_active=True):
        return f(self, mesg, is_active=True)
    return _always_active

def prepend_tag(tag):
    def _prepend_tag(f):
        def wrapper(self, mesg: str, is_active=True):
            if is_active:
                return f(self, "{0:12s}: {1}".format('['+tag+']', mesg))
        return wrapper
    return _prepend_tag

class Logger:

    def __init__(self, file_name=None):
        self.out = None
        if file_name is not None:
            self.out = open(file_name, "w")

    def __del__(self):
        if self.out is not None:
            self.out.close()

    def print(self, mesg):
        print(mesg, file=self.out)

    @prepend_tag("Info")
    def info(self, mesg: str, is_active=True) -> None:
        print(mesg, file=self.out)

    @always_active
    @prepend_tag("Warning")
    def warning(self, mesg: str, is_active=True) -> None:
        print(mesg, file=self.out)

    @always_active
    @prepend_tag("Error")
    def error(self, mesg: str, is_active=True) -> None:
        print(mesg, file=self.out)

class TimeStamp:

    def __init__(self, user_string=None, db_string=None):
        self.user_format = "%d.%m.%Y-%H:%M"
        self.db_format = "%Y-%m-%d %H:%M"
        self.date_time = None

        if db_string:
            self.date_time = datetime.strptime(db_string, self.db_format)
        elif user_string and TimeStamp.time_conforms_format(user_string, self.user_format):
            try:
                self.date_time = datetime.strptime(user_string, self.user_format)
            except ValueError:
                raise
        else:
            self.date_time = datetime.now()

    @staticmethod
    def time_conforms_format(time_string, time_format):
        try:
            datetime.strptime(time_string, time_format)
        except ValueError:
            return False
        return True

    def datetime(self):
        return self.date_time

    def db_string(self):
        return self.date_time.strftime(self.db_format)

    def __str__(self):
        return self.date_time.strftime(self.user_format)

    def __repr__(self):
        return self.__str__()

    def day(self) -> int:
        return self.date_time.day

    def month(self) -> int:
        return self.date_time.month

    def year(self) -> int:
        return self.date_time.year

    def hour(self) -> int:
        return self.date_time.hour

    def minute(self) -> int:
        return self.date_time.minute

    def __sub__(self, other):
        return self.datetime() - other.datetime()

class TimeInterval:
    def __init__(self,begin: TimeStamp, end: TimeStamp):
        if begin.date_time > end.date_time:
            raise ValueError('Start ({}) must not be greater than end ({})'.format(begin, end))
        self.begin = begin
        self.end = end

    def __str__(self):
            return "[{}, {}]".format(self.begin, self.end)
    def __lt__(self, other):
        return self.begin.date_time < other.begin.date_time and self.end.date_time < other.begin.date_time

    def __gt__(self, other):
        return other < self

    def __le__(self, other):
        return self.begin.date_time < other.begin.date_time     \
                and self.end.date_time >= other.begin.date_time \
                and self.end.date_time <= other.end.date_time

    def __ge__(self, other):
        return other <= self

    def contains(self, other):
        return self.begin.date_time <= other.begin.date_time \
               and other.end.date_time <= self.end.date_time

    def disjunct(self, other):
        return self < other or self > other

    def overlapps(self, other):
        return self <= other or self >= other

    def intersection(self, other):
        """Returns the intersecting time as datetime.timedelta"""
        if self.overlapps(other):
            if self <= other:
                return  self.end - other.begin
            else:
                return  other.end - self.begin
        elif self.contains(other):
            return other.end - other.begin
        elif other.contains(self):
            return self.end - self.begin
        else:
            return timedelta(days=0, seconds=0)
