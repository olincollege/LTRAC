"""
Classes for creating a workout routine for LTRAC
"""

import json
from datetime import date
from typing import Dict, List
import pandas as pd
from flask import request


class Exercise:
    """
    A gym exercise with number of sets

    Attributes:
        name: A string representing the name of the routine
        sets: An integer representing the number of sets for the exercise
        history: A dictionary mapping strings of dates to a list of integers,
            representing the weights used on that day. The length of the list
            will be equal to the number of sets.
    """

    _name: str
    _sets: int
    _history: Dict[str, List[int]]

    def __init__(self, name: str, sets: int):
        self._name = name
        self._sets = sets
        self._history = {}

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def name(self):
        """
        Return private attribute name
        """
        return self._name

    @property
    def sets(self):
        """
        Return private attribute sets
        """
        return self._sets

    @property
    def history(self):
        """
        Return private attribute history
        """
        return self._history

    @classmethod
    def from_input(cls, name_id: str, sets_id: str):
        """
        Create exercise from Flask input

        Args:
            name_id: A string representing the html variable label for the name
                of the exercise
            sets_id: A string representing the html variable label for the
                number of sets for the exercise

        Returns:
            An Exercise object with the name and sets
        """
        return cls(request.args.get(name_id), request.args.get(sets_id))

    def log_weights(self, date_iso: str, weights: str):
        """
        Log weights used for exercise for today

        Args:
            date: A string representing the date in ISO format (YYYY-MM-DD)
            weights: A list of integers representing the weights used in the
                exercise. Length of list should be equal to the number of sets
                for the exercise.

        Raises:
            ValueError: Inputted number of weights does not match number of
                sets for the exercise
        """
        if len(weights) != int(self.sets):
            raise ValueError(
                "Number of weights logged does not match number of sets"
            )
        self.history[date_iso] = weights

    def log_weights_today(self, weights: List[int]):
        """
        Log weights used for exercise for today

        Args:
            weights: A list of integers representing the weights used in the
                exercise. Length of list should be equal to the number of sets
                for the exercise.
        """
        self.log_weights(date.today().isoformat(), weights)

    def personal_record(self):
        """
        Find the highest weight logged for the exercise

        Returns:
            An integer representing the highest weight logged. Returns None if
            history is empty
        """
        if not self.history:
            return None
        return max(sum([weights for _, weights in self.history.items()], []))


class Routine:
    """
    An exercise routine storing user inputted exercises

    Attributes:
        exercises: A dictionary mapping the string of the exercise name to the
            corresponding exercise object
        name: A string representing the name of the routine
    """

    _exercises: Dict[str, Exercise]
    _name: str

    def __init__(self, name: str):
        self._exercises = {}
        self._name = name

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def exercises(self):
        """
        Return private attribute exercises
        """
        return self._exercises

    @property
    def name(self):
        """
        Return private attribute name
        """
        return self._name

    @classmethod
    def from_input(cls, name_id: str):
        """
        Create Routine from Flask input

        Args:
            name_id: A string representing the html variable label for the name
                of the routine
        """
        return cls(request.args.get(name_id))

    @classmethod
    def from_json(cls, file_path: str):
        """
        Create routine from json file

        Args:
            file_path: A string representing the path to the json file
        """
        with open(file_path, "r", encoding="UTF-8") as file:
            json_dict = json.load(file)
        routine = Routine(json_dict["_name"])
        for key, item in json_dict["_exercises"].items():
            exercise = Exercise(item["_name"], item["_sets"])
            routine.exercises[key] = exercise
        return routine

    def add_exercise(self, exercise: Exercise):
        """
        Add an exercise to the routine

        Args:
            exercise: An Exercise object to be added to the routine
        """
        self.exercises[exercise.name] = exercise

    def add_exercise_from_input(self, name_id: str, sets_id: str):
        """
        Add an exercise to the routine from user input through the website

        Args:
            name_id: A string representing the html variable label for the name
                of the exercise
            sets_id: A string representing the html variable label for the
                number of sets for the exercise
        """
        exercise = Exercise.from_input(name_id, sets_id)
        self.add_exercise(exercise)

    def to_json(self, file_path: str):
        """
        Export routine to json file

        Args:
            file_path: A string representing the path to the json file
        """
        json_dict = self.__dict__.copy()
        json_dict["_exercises"] = {
            key: {"_name": ex.name, "_sets": ex.sets}
            for key, ex in json_dict["_exercises"].items()
        }
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(json.dumps(json_dict, indent=4))

    def export_log(self, file_path: str):
        """
        Export history of each exercise to single csv

        Args:
            file_path: A string representing the path to the csv file
        """
        log_df = pd.DataFrame()
        for _, ex in self.exercises.items():
            ex_df = pd.DataFrame(ex.history)
            ex_df.insert(0, "Exercise", [ex.name] * int(ex.sets))
            ex_df.insert(1, "Set", list(range(1, int(ex.sets) + 1)))
            log_df = pd.concat([log_df, ex_df], ignore_index=True)
        log_df.to_csv(file_path)

    def load_log(self, file_path: str):
        """
        Load history of each exercise from csv. Assumes the routine is already
        initialized with matching exercises through json.

        Args:
            file_path: A string representing the path to the csv file
        """
        routine_df = pd.read_csv(file_path, index_col=0)
        for _, ex in self.exercises.items():
            ex_df = routine_df[routine_df["Exercise"] == ex.name]
            days = list(routine_df.columns[2:])
            for day in days:
                if not all(ex_df[day].isna()):
                    ex.log_weights(day, list(ex_df[day]))
