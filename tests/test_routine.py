"""
Unit tests for Routine class
"""

import sys
import os
import json
import pytest

sys.path.append("./")

# pylint: disable=import-error, wrong-import-position
from modules.workouts import Routine, Exercise


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
def sample_routine():
    """
    Create a sample routine with exercises to be used for testing

    Returns:
        A routine object with exercises
    """
    routine = Routine("routine1")
    routine.add_exercise(Exercise("exercise1", 2))
    routine.add_exercise(Exercise("exercise2", 2))
    return routine


@pytest.fixture
# pylint: disable=redefined-outer-name
def sample_routine_with_log(sample_routine: Routine):
    """
    Create a sample routine with logged exercises

    Returns:
        A routine object with logged exercises
    """
    routine = sample_routine
    routine.exercises["exercise1"].log_weights("2023-04-30", [1, 2])
    routine.exercises["exercise2"].log_weights("2023-04-30", [1, 2])
    return routine


# pylint: disable=redefined-outer-name
def test_to_json(sample_routine_with_log: Routine):
    """
    Test that Routine.to_json creates a json file that matches the expected
    structure

    Args:
        sample_routine: The Routine object to use
    """
    sample_routine_with_log.to_json("user_data/routine1.json")
    with open(
        "user_data/routine1.json", "r", encoding="UTF-8"
    ) as created_json, open(
        "static_data/routines/routine1/routine1.json", "r", encoding="UTF-8"
    ) as target_json:
        assert json.load(created_json) == json.load(target_json)


def test_from_json(sample_routine: Routine):
    """
    Test that Routine.from_json creates a Routine object with properly set
    attributes

    Args:
        sample_routine_with_log: The Routine object to compare correctness
    """
    assert (
        Routine.from_json("static_data/routines/routine1/routine1.json")
        == sample_routine
    )