#!/usr/bin/env python3
from enum import Enum
from datetime import date, timedelta, datetime
from calendar import monthrange

class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def last_dow(d = date.today(), dow: Weekday = Weekday.MONDAY, weeks_ago=0):

    return d - timedelta(days=d.weekday(), weeks=weeks_ago) + timedelta(days=dow.value)


def last_day_of_month(year, month):
    return monthrange(year, month)[1]


def string_to_date(s):
    return date(int(s[:4]),int(s[4:6]),int(s[6:]))


def add_minutes_to_time(t, minutes):
    d = datetime(100, 1, 1, t.hour, t.minute, t.second)
    d = d + timedelta(minutes=minutes)
    return d.time()


def add_minutes_to_date(d, t, minutes):
    date = datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
    date = date + timedelta(minutes=minutes)
    return date.date()


if __name__ == '__main__':
    pass