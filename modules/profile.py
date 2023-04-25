"""
Functions for creating new users and viewing stats in LTRAC
"""


class User:
    """
    A LTRAC user profile

    Attributes:
        name: A string representing the name of the user
        xp_points: An integer representing the amount of experience points
            the user has
        routines: A dictionary of routine objects representing the user's
            workout routines
    """

    def __init__(self, name, xp_points=0):
        self.name = name
        self.xp_points = xp_points
        self.routines = {}
