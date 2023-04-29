"""
Functions for creating new users and viewing stats in LTRAC
"""
import json
import os
from datetime import date, timedelta
from typing import Dict, List
from flask import request
from .workouts import Routine
from .dates import Weekday


class User:
    """
    A LTRAC user profile

    Attributes:
        name: A string representing the name of the user
        xp_points: An integer representing the amount of experience points
            the user has
        routines: A dictionary mapping the string of the routine name to the
            corresponding routine object, representing the user's workout
            routines
        workout_days: A dictionary mapping Weekday objects to booleans,
            representing the days the user plans to workout
    """

    XP_PER_LEVEL = 1000

    _name: str
    _xp_points: int
    _routines: Dict[str, Routine]
    _workout_days: Dict[Weekday, bool]

    def __init__(self, name: int, xp_points: int = 0):
        self._name = name
        self._xp_points = xp_points
        self._routines = {}
        self._workout_days = {
            Weekday.MONDAY: False,
            Weekday.TUESDAY: False,
            Weekday.WEDNESDAY: False,
            Weekday.THURSDAY: False,
            Weekday.FRIDAY: False,
            Weekday.SATURDAY: False,
            Weekday.SUNDAY: False,
        }

    @property
    def name(self):
        """
        Return private attribute name
        """
        return self._name

    @property
    def xp_points(self):
        """
        Return private attribute xp_points
        """
        return self._xp_points

    @property
    def routines(self):
        """
        Return private attribute routines
        """
        return self._routines

    @property
    def workout_days(self):
        """
        Return private attribute workout_days
        """
        return self._workout_days

    @classmethod
    def load_user_data(cls, user_name: str):
        """
        Load user data from user json as well as all associated routine data

        Args:
            user_name: A string representing the user's name to load
        """
        name_no_spaces = user_name.replace(" ", "_")

        # load user json
        with open(
            f"user_data/{name_no_spaces}/{name_no_spaces}.json",
            "r",
            encoding="UTF-8",
        ) as file:
            json_dict = json.load(file)

        # set user data from json
        user = cls(json_dict["_name"], json_dict["_xp_points"])
        user.set_workout_days(
            [
                Weekday[day]
                for day, value in json_dict["_workout_days"].items()
                if value
            ]
        )

        # load routine json and csv
        for routine_name in json_dict["_routines"]:
            routine_name_no_spaces = routine_name.replace(" ", "_")
            # pylint: disable=line-too-long
            path = f"user_data/{name_no_spaces}/{routine_name_no_spaces}/{routine_name_no_spaces}"
            user.add_routine(Routine.from_json(f"{path}.json"))
            user.routines[routine_name].load_log(f"{path}.csv")
        return user

    def level(self):
        """
        Calculate the level of the user

        Returns:
            An integer representing the user's level
        """
        return self.xp_points // self.XP_PER_LEVEL

    def gain_xp(self, gained_xp: int):
        """
        Gain an amount of xp for completing a workout

        Args:
            gained_xp: An integer representing the amount of xp gained
        """
        self.xp_points += gained_xp

    def add_routine(self, routine: Routine):
        """
        Add a routine to the user's routines

        Args:
            routine: A Routine object to be added to the user's routines
        """
        self.routines[routine.name] = routine

    def set_workout_days(self, selected_days: List[Weekday]):
        """
        Set which days to workout

        Args:
            selected_days: A list of Weekday objects, representing the days
                to workout on
        """
        for day in self.workout_days:
            if day in selected_days:
                self.workout_days[day] = True
            else:
                self.workout_days[day] = False

    def next_workout_day(self):
        """
        Determine the next day after today that the user should workout based
        on user's workout days

        Returns:
            A datetime.date object representing the next day the user has
            planned to workout on. Returns None if no workout days are set
        """
        # get the day numbers of the user's workout days
        # (monday = 0, tuesday = 1, etc)
        workout_day_numbers = [
            day.value for day, value in self.workout_days.items() if value
        ]

        # return None if user has no workout days set
        if not workout_day_numbers:
            return None

        today = date.today()
        today_number = date.weekday(today)

        try:
            # do this if there's a workout day upcoming in the week
            next_day_delta = (
                min(day for day in workout_day_numbers if day > today_number)
                - today_number
            )
        except ValueError:
            # do this if the next workout day is next week
            next_day_delta = min(workout_day_numbers) - today_number + 7

        return today + timedelta(days=next_day_delta)

    def log_workout(self, routine_name: str):
        """
        Log all exercises in a routine by pulling from user inputted values in
        Flask, then gain xp

        Args:
            routine_name: A string representing the routine to log
        """
        for _, exercise in self.routines[routine_name].exercises.items():
            current_exercise = exercise.name
            weight_list = [
                request.form[f"{current_exercise} {i}"]
                for i in range(int(exercise.sets))
            ]
            exercise.log_weights_today(weight_list)
        self.gain_xp(100)

    def to_json(self):
        """
        Export user to json file in the directory 'user_data/[USERNAME]' with
        the name '[USERNAME].json' Creates the directory if it doesn't exist
        already
        """
        json_dict = self.__dict__.copy()
        json_dict["_routines"] = list(json_dict["_routines"].keys())
        json_dict["_workout_days"] = {
            day.name: value for day, value in json_dict["_workout_days"].items()
        }

        name_no_spaces = self.name.replace(" ", "_")
        dir_path = f"user_data/{name_no_spaces}"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        with open(
            f"{dir_path}/{name_no_spaces}.json", "w", encoding="UTF-8"
        ) as file:
            file.write(json.dumps(json_dict, indent=4))

    def export_routines(self):
        """
        Export user's routines to json and exercise logs to csv in the
        directory 'user_data/[USERNAME]/[ROUTINE_NAME]' with the name
        '[ROUTINE_NAME].json' and '[ROUTINE_NAME].csv'
        """
        name_no_spaces = self.name.replace(" ", "_")
        user_dir = f"user_data/{name_no_spaces}"

        for _, routine in self.routines.items():
            routine_name_no_spaces = routine.name.replace(" ", "_")
            routine_dir = f"{user_dir}/{routine_name_no_spaces}"
            if not os.path.exists(routine_dir):
                os.mkdir(routine_dir)

            routine.export_log(f"{routine_dir}/{routine_name_no_spaces}.csv")
            routine.to_json(f"{routine_dir}/{routine_name_no_spaces}.json")
