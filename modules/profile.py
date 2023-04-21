"""
Functions for creating new users and viewing stats in LTRAC
"""

from flask import request


class User:
    """
    A LTRAC user profile
    """

    def __init__(self, name, level):
        self.name = name
        self.level = level