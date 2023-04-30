"""
Unit tests for User class
"""

import sys
import os
import json
import shutil
import pytest

sys.path.append("./")

# pylint: disable=import-error, wrong-import-position
from modules.profile import User
from modules.workouts import Routine
from modules.dates import Weekday


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    """
    Change working directory to tests directory
    """
    monkeypatch.chdir(request.fspath.dirname)


@pytest.fixture(autouse=True)
def create_user_data_dir():
    """
    Create user_data directory if it doesn't exist
    """
    if not os.path.exists("user_data"):
        os.mkdir("user_data")


@pytest.fixture
def sample_user():
    """
    Create a sample user to be used for testing

    Returns:
        An user object with the name "username"
    """
    return User("username")


# pylint: disable=redefined-outer-name
def test_to_json_creates_path(sample_user: User):
    """
    Test that User.to_json creates the user directory if it doesn't exist

    Args:
        sample_user: The User object to use
    """
    if os.path.exists("user_data/username"):
        shutil.rmtree("user_data/username")
    try:
        sample_user.to_json()
    except FileNotFoundError:
        assert False


def test_to_json_correctness(sample_user: User):
    """
    Test that User.to_json creates a json file that matchs the expected file
    structure

    Args:
        sample_user: The User object to use
    """
    sample_user.to_json()
    with open(
        "user_data/username/username.json", encoding="UTF-8"
    ) as created_json, open(
        "static_data/username/username.json", encoding="UTF-8"
    ) as target_json:
        assert json.load(created_json) == json.load(target_json)


load_user_cases = [
    ("username", {}),
    ("user_with_xp", {"xp_points": 1000}),
    (
        "user_with_workout_days",
        {"workout_days": [Weekday.MONDAY, Weekday.THURSDAY, Weekday.FRIDAY]},
    ),
    ("user_with_routines", {"routines": ["routine1", "routine2"]}),
]


@pytest.mark.parametrize("name,attr_dict", load_user_cases)
def test_load_user(name: str, attr_dict: dict):
    """
    Test that User.load_user_data() loads correctly by comparing the loaded
    user to a user constructed through attr_dict

    Args:
        name: A string representing the name of the user to load
        attr_dict: A dictionary to construct the solution user. Has three
            possible keys: xp_points, workout_days, and routines
                - xp_points maps to an integer representing how much xp the
                    user has
                - workout_days maps to a list of Weekday objects, representing
                    the days the user plans to workout
                - routines maps to a list of strings, representing the names of
                    the user's routines
    """
    target_user = User(name)
    if attr_dict.get("xp_points"):
        target_user.gain_xp(attr_dict["xp_points"])
    if attr_dict.get("workout_days"):
        target_user.set_workout_days(attr_dict["workout_days"])
    if attr_dict.get("routines"):
        for routine in attr_dict["routines"]:
            target_user.add_routine(
                Routine.from_json(
                    f"static_data/{name}/{routine}/{routine}.json"
                )
            )
    loaded_user = User.load_user_data(name, directory="static_data")
    assert loaded_user == target_user
