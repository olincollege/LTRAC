"""
Functions for creating new users and viewing stats in LTRAC
"""
from enum import Enum


class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


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
        self.workout_days = {
            Weekday.MONDAY: False,
            Weekday.TUESDAY: False,
            Weekday.WEDNESDAY: False,
            Weekday.THURSDAY: False,
            Weekday.FRIDAY: False,
            Weekday.SATURDAY: False,
            Weekday.SUNDAY: False,
        }

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

    def set_workout_days(self, selected_days):
        """
        Set which days to workout

        args:
            selected_days: A list of Weekday objects, representing the days
                to workout on
        """
        for day in self.workout_days:
            if day in selected_days:
                self.workout_days[day] = True
            else:
                self.workout_days[day] = False
