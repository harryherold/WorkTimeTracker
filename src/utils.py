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

# TODO Implement subraction of time stamps
def sub_timestamps(t1: TimeStamp, t2: TimeStamp) -> TimeStamp:
    pass

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
