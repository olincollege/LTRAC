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
