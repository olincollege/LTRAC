"""
Functions for creating new users and viewing stats in LTRAC
"""
import json
import os
from dates import Weekday
from plan import Routine
from flask import request


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

    @classmethod
    def load_user_data(cls, user_name):
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
        user = cls(json_dict["name"], json_dict["xp_points"])
        user.set_workout_days(
            [
                Weekday[day]
                for day, value in json_dict["workout_days"].items()
                if value
            ]
        )

        # load routine json and csv
        for routine_name in json_dict["routines"]:
            routine_name_no_spaces = routine_name.replace(" ", "_")
            path = f"user_data/{name_no_spaces}/{routine_name_no_spaces}/{routine_name_no_spaces}"
            user.add_routine(Routine.from_json(f"{path}.json"))
            user.routines[routine_name].load_log(f"{path}.csv")
        return user

    def level(self):
        """
        Calculate the level of the user
        """
        return self.xp_points // self.XP_PER_LEVEL

    def gain_xp(self, gained_xp):
        """
        Gain an amount of xp for completing a workout

        Args:
            gained_xp: An integer representing the amount of xp gained
        """
        self.xp_points += gained_xp

    def add_routine(self, routine):
        """
        Add a routine to the user's routines

        Args:
            routine: A Routine object to be added to the user's routines
        """
        self.routines[routine.name] = routine

    def set_workout_days(self, selected_days):
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

    def log_workout(self, routine_name):
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
        json_dict["routines"] = list(json_dict["routines"].keys())
        json_dict["workout_days"] = {
            day.name: value for day, value in json_dict["workout_days"].items()
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
