""""
Unit tests for the dates module.
"""
import datetime
import sys

sys.path.append("./")

# pylint: disable=import-error, wrong-import-position
from modules.dates import Weekday, get_week


def test_week_string():
    """
    Test that get_week() only accepts strings.
    """
    assert get_week(12343) == "TypeError: Date needs to be a string."


def test_string_format():
    """
    Test that get_week() only accepts strings in ISO format. This would entail
    a date formatted year-month-day.
    """

    assert (
        get_week("2023-24-12")
        == "ValueError: Date is not a string in ISO format."
    )


def test_datetime_object():
    """
    Test that get_week() properly accepts a string-converted datetime date object.
    """
    today = str(datetime.date.today())
    assert str(get_week(str(datetime.date.today()))[-1]) == today


def test_weekday_object():
    """
    Test that the Weekday object properly returns values for dates.
    """
    assert isinstance(get_week()[0][0], type(Weekday(0))) is True
