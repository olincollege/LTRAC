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

    XP_PER_LEVEL = 1000

    def __init__(self, name, xp_points=0):
        self.name = name
        self.xp_points = xp_points
        self.routines = {}

    def level(self):
        """
        Calculate the level of the user
        """
        return self.xp_points // self.XP_PER_LEVEL

    def add_routine(self, routine):
        """
        Add a routine to the user's routines

        args:
            routine: A Routine object to be added to the user's routines
        """
        self.routines[routine.name] = routine
