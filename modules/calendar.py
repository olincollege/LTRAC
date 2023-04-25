"""
Function for extracting date information for the current week.
"""
import datetime


def get_week():
    """
    Based on the current date, finds the numerical day values
    for every day in the current week.
    Returns:
        week_dates: A list of tuples which contain the name of the day,
        followed by the numerical day value.
    """
    today = datetime.date.today()
    weekday = datetime.date.weekday(today)
    weekdays = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }
    start_of_week = today - datetime.timedelta(days=weekday)
    week_dates = []
    for i in range(7):
        week_date = (start_of_week + datetime.timedelta(days=i)).day
        week_date = (weekdays[i], week_date)
        week_dates.append(week_date)
    return week_dates
