import math

class Duration:
    """
    Represents a duration of time in years, days, hours, minutes, and seconds.

    Attributes:
        sec (int): Seconds.
        min (int): Minutes.
        hour (int): Hours.
        day (int): Days.
        year (float): Years, including fractional part.

    Note:
        The parameters values can be floats!
    """

    def __init__(self, sec: int = 0, min: int = 0, hour: int = 0, day: int = 0, year: int = 0) -> None:
        assert sec >= 0 and min >= 0 and hour >= 0 and day >= 0 and year >= 0, "!Duration can't be negative!"
        # We deal with the cas where there is fractional parts in the parameters. We thus redirect the fractional parts in the seconds part.
        self.day, self.year = math.modf(year)
        self.day *= 365
        self.day += day
        self.hour, self.day = math.modf(self.day)
        self.hour *= 24
        self.hour += hour
        self.min, self.hour = math.modf(self.hour)
        self.min *= 60
        self.min += min
        self.sec, self.min = math.modf(self.min)
        self.sec *= 60
        self.sec += sec
        # We now store the parameters following the standard time format.
        min, self.sec = divmod(self.sec, 60)
        self.min += min
        hour, self.min = divmod(self.min, 60)
        self.hour += hour
        day, self.hour = divmod(self.hour, 24)
        self.day += day
        year, self.day = divmod(self.day, 365)
        self.year += year

    def __add__(self, other):
        min, sec = divmod(self.sec + other.sec, 60)
        hour, min = divmod(min + self.min + other.min, 60)
        day, hour = divmod(hour + self.hour + other.hour, 24)
        year, day = divmod(day + self.day + other.day, 365)
        year += self.year + other.year
        return Duration(sec, min, hour, day, year)

    def __str__(self) -> str:
        return f"{self.year}y {self.day}d {self.hour}h {self.min}m {self.sec}s"

    def __sub__(self, other):
        self_sec = self.to_sec()
        other_sec = other.to_sec()
        assert self_sec >= other_sec, "!The first Duration can't be smaller than the second!"
        return Duration(self_sec - other_sec)

    """ Comparison methods """

    def __eq__(self, other):
        return math.isclose(self.to_sec(), other.to_sec())

    def __le__(self, other):
        return self.to_sec() <= other.to_sec()

    def __lt__(self, other):
        return self.to_sec() < other.to_sec()

    def to_sec(self):
        return self.year * 365 * 24 * 60 * 60 + self.day * 24 * 60 * 60 + self.hour * 60 * 60 + self.min * 60 + self.sec
    
    def to_min(self):
        return self.year * 365 * 24 * 60 + self.day * 24 * 60 + self.hour * 60 + self.min + self.sec / 60
    
    def to_hour(self):
        return self.year * 365 * 24 + self.day * 24 + self.hour + self.min / 60 + self.sec / 3600
    
    def to_day(self):
        return self.year * 365 + self.day + self.hour / 24 + self.min / 1440 + self.sec / 86400
    
    def to_year(self):
        return self.year + self.day / 365 + self.hour / 8760 + self.min / 525600 + self.sec / 31536000
    
class DurationInt(Duration):
    """ It's an integer version of Duration. It helps to deals with great integers since Python is better at manipulating great integers rather than floats. """
    
    def __init__(self, sec=0, min=0, hour=0, day=0, year=0):
        assert type(sec) == int and type(min) == int and type(hour) == int and type(day) == int and type(year) == int, "!DurationInt must be an integer!"
        assert sec >= 0 and min >= 0 and hour >= 0 and day >= 0 and year >= 0, "!Duration can't be negative!"
        
        self.min, self.sec = divmod(sec, 60)
        self.min += min
        self.hour, self.min = divmod(self.min, 60)
        self.hour += hour
        self.day, self.hour = divmod(self.hour, 24)
        self.day += day
        self.year, self.day = divmod(self.day, 365)
        self.year += year

if __name__ == '__main__':
    import duration
    print(help(duration))
