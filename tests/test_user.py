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
        "target_data/username.json", encoding="UTF-8"
    ) as target_json:
        assert json.load(created_json) == json.load(target_json)
