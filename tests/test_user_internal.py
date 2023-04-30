"""
Unit tests for the User class internal methods
"""

import sys
import pytest


sys.path.append("./")

# pylint: disable=import-error, wrong-import-position
from modules.profile import User


@pytest.fixture
def sample_user():
    """
    Create a sample user to be used for testing

    Returns:
        A user object with the name "username"
    """
    return User("username")
