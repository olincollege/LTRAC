"""
Unit tests for Routine class
"""

import sys
import os
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
    Create a sample routine with logged exercises to be used for testing

    Returns:
        A routine object with logged exercises
    """
    routine = Routine("routine1")
    routine.add_exercise(Exercise("exercise1", 2))
    routine.add_exercise(Exercise("exercise2", 2))
    routine.exercises["exercise1"].log_weights("2023-04-30", [1, 2])
    routine.exercises["exercise2"].log_weights("2023-04-30", [1, 2])
    return routine
