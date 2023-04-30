"""
Unit tests for Exercise class
"""

import sys
import pytest

sys.path.append("./")

# pylint: disable=import-error, wrong-import-position
from modules.workouts import Exercise


@pytest.fixture
def sample_exercise():
    """
    Create a sample exercise to be used for testing

    Returns:
        An Exercise object with the name "sample" and sets equal to 3
    """
    return Exercise("sample", 3)


# pylint: disable=redefined-outer-name
def test_weights_get_logged(sample_exercise: Exercise):
    """
    Test that the method logged exercises appear in the exercise's history

    Args:
        sample_exercise: The Exercise object to use
    """
    exercise = sample_exercise
    exercise.log_weights_today([1, 2, 3])
    assert exercise.history.popitem()[1] == [1, 2, 3]
