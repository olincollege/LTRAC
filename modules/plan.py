"""
Classes for creating a workout routine for LTRAC
"""

import json
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

    def __init__(self, name, sets):
        self.name = name
        self.sets = sets
        self.history = {}

    @classmethod
    def from_input(cls, name_id, sets_id):
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

    def log_weights(self, weights):
        """
        Log weights used for exercise on a single day

        Args:
            weights: A list of integers representing the weights used in the
                exercise. Length of list should be equal to the number of sets
                for the exercise.
        """
        pass

    def __repr__(self):
        return f"{self.name}, {self.sets}"


class Routine:
    """
    An exercise routine storing user inputted exercises

    Attributes:
        exercises: A dictionary mapping the string of the exercise name to the
            corresponding exercise object
        name: A string representing the name of the routine
    """

    def __init__(self, name):
        self.exercises = {}
        self.name = name

    @classmethod
    def from_input(cls, name_id):
        """
        Create Routine from Flask input

        Args:
            name_id: A string representing the html variable label for the name
                of the routine
        """
        return cls(request.args.get(name_id))

    @classmethod
    def from_json(cls, file_path):
        """
        Create routine from json file

        Args:
            file_path: A string representing the path to the json file
        """
        with open(file_path, "r", encoding="UTF-8") as file:
            json_dict = json.load(file)
        routine = Routine(json_dict["name"])
        for key, item in json_dict["exercises"].items():
            exercise = Exercise(item["name"], item["sets"])
            routine.exercises[key] = exercise
        return routine

    def add_exercise(self, exercise):
        """
        Add an exercise to the routine

        Args:
            exercise: An Exercise object to be added to the routine
        """
        self.exercises[exercise.name] = exercise

    def add_exercise_from_input(self, name_id, sets_id):
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

    def to_json(self, file_path):
        """
        Export routine to json file

        Args:
            file_path: A string representing the path to the json file
        """
        json_dict = self.__dict__.copy()
        json_dict["exercises"] = {
            key: ex.__dict__ for key, ex in json_dict["exercises"].items()
        }
        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(json.dumps(json_dict, indent=4))

    def __repr__(self):
        return " ".join([ex.__repr__() for ex in self.exercises.items()])
