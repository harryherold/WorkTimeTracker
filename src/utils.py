from datetime import datetime


def print_info(mesg: str, is_active=True):
    if is_active:
        print("[Info]    : {}".format(mesg))


def print_warning(mesg: str, is_active=True):
    if is_active:
        print("[Warning] : {}".format(mesg))


def print_error(mesg: str, is_active=True):
    if is_active:
        print("[Error]   : {}".format(mesg))


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