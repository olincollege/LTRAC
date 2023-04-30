"""
Unit tests for the User class internal methods
"""

import sys
from typing import List
import pytest

sys.path.append("./")

# pylint: disable=import-error, wrong-import-position
from modules.profile import User
from modules.workouts import Routine
from modules.dates import Weekday


@pytest.fixture
def sample_user():
    """
    Create a sample user to be used for testing

    Returns:
        A user object with the name "username"
    """
    return User("username")


# pylint: disable=redefined-outer-name
def test_gain_xp(sample_user: User):
    """
    Test that User.gain_xp adds the correct ammount of xp to the User

    Args:
        sample_user: The User object to use
    """
    xp_gain = 1000
    sample_user.gain_xp(xp_gain)
    assert sample_user.xp_points == xp_gain


level_cases = [(0, 0), (1000, 1), (1001, 1), (999, 0)]


@pytest.mark.parametrize("xp_gain,level", level_cases)
def test_level(sample_user: User, xp_gain: int, level: int):
    """
    Test that User.level returns the correct level based on a variable ammount
    of xp gained

    Args:
        sample_user: The User object to use
        xp_gain: An integer representing how much xp the user will gain
        level: An integer represetning the expected level based on the ammount
            of xp gained
    """
    sample_user.gain_xp(xp_gain)
    assert sample_user.level() == level


add_routine_cases = [
    # test adding one routine
    [Routine("routine1")],
    # test adding multiple routines
    [Routine("routine1"), Routine("routine2"), Routine("routine3")],
]


@pytest.mark.parametrize("routines", add_routine_cases)
def test_add_routine(sample_user: User, routines: List[Routine]):
    """
    Test that User.add_routine properly adds the routine

    Args:
        sample_user: The User object to use
        routines: A list of Routine objects to be added to the User's routines
    """
    for routine in routines:
        sample_user.add_routine(routine)
    assert all(
        sample_user.routines[routine.name] == routine for routine in routines
    )


set_workout_days_cases = [
    # test setting one day
    [Weekday.MONDAY],
    # test setting multiple days
    [Weekday.MONDAY, Weekday.THURSDAY, Weekday.FRIDAY],
]


@pytest.mark.parametrize("days", set_workout_days_cases)
def test_set_workout_days(sample_user: User, days: List[Weekday]):
    """
    Test that User.set_workout_days properly sets workout days

    Args:
        sample_user: The User object to use
        days: A list of Weekday objects to be set as the User's workout days
    """
    sample_user.set_workout_days(days)
    assert {
        day for day, value in sample_user.workout_days.items() if value
    } == set(days)
