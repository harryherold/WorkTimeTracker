from datetime import datetime


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

    def __init__(self, time_string):
        self.format = "%d.%m.%Y-%H:%M"
        self.date_time = None
        # TODO string processing in separate unit
        if 'c' == time_string:
            self.date_time = datetime.now()
        else:
            try:
                self.date_time = datetime.strptime(time_string, self.format)
            except ValueError:
                raise

    def datetime(self):
        return self.date_time

    def __str__(self):
        return self.date_time.strftime(self.format)

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
        """Returns a tuple(days,hours,mins) for the difference between two timestamps"""
        diff = self.datetime() - other.datetime()
        days = diff.days
        hours = int(diff.seconds / 3600)
        mins = int((diff.seconds - (hours * 3600)) / 60)
        return (days, hours, mins)


# TODO Implement TimeInterval class
class TimeInterval:
    def __init__(self,begin: TimeStamp, end: TimeStamp):
        if begin.date_time > end.date_time:
            raise ValueError('Start ({}) must not be greater than end ({})'.format(begin, end))
        self.begin = begin
        self.end = end

    def intersects(self, other):
        if self < other or other < self:
            return False
        if self <= other or other <= self:
            return True
        if self.contains(other) or other.contains(self):
            return True

    def __lt__(self, other):
        return self.begin.date_time < other.begin.date_time and self.end.date_time < other.begin.date_time

    def __le__(self, other):
        return self.begin.date_time < other.begin.date_time     \
                and self.end.date_time >= other.begin.date_time \
                and self.end.date_time <= other.end.date_time

    def contains(self, other):
        return self.begin.date_time <= other.begin.date_time \
               and other.end.date_time <= self.end.date_time
