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


def get_week(today=str(datetime.date.today())):
    """
    Based on the current date, finds the numerical day values
    for every day in the current week.

    Args:
        today: a datetime.date object representing the current date.
    Returns:
        A list of tuples which contain a Weekday object representing the name
        of the day, followed by the numerical day value.
    """
    if isinstance(today, str) is False:
        return "TypeError: Date needs to be a string."
    try:
        datetime.datetime.fromisoformat(today)
        today = datetime.date.fromisoformat(today)
    except ValueError:
        return "ValueError: Date is not a string in ISO format."

    weekday = datetime.date.weekday(today)
    start_of_week = today - datetime.timedelta(days=weekday)
    week_dates = [
        (
            Weekday(day_number),
            (start_of_week + datetime.timedelta(days=day_number)).day,
        )
        for day_number in range(7)
    ]
    week_dates.append(today)
    return week_dates
