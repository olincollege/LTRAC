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
