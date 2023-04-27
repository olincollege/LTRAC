"""
Function for extracting date information for the current week.
"""
import datetime
from enum import Enum


class Weekday(Enum):
    """
    Days of the week, starting with Monday as 0
    """

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def get_week():
    """
    Based on the current date, finds the numerical day values
    for every day in the current week.

    Returns:
        A list of tuples which contain a Weekday object representing the name
        of the day, followed by the numerical day value.
    """
    today = datetime.date.today()
    weekday = datetime.date.weekday(today)
    start_of_week = today - datetime.timedelta(days=weekday)
    week_dates = []
    for i in range(7):
        week_date = (start_of_week + datetime.timedelta(days=i)).day
        week_date = (Weekday(i), week_date)
        week_dates.append(week_date)
    return week_dates
