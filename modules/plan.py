from flask import request


class Exercise:
    def __init__(self, name_id, sets_id):
        self.name = request.args.get(name_id)
        self.sets = request.args.get(sets_id)

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

    def __init__(self, name_id):
        self.exercises = {}
        self.name = request.args.get(name_id)

    def add_exercise(self, name_id, sets_id):
        """
        Add an exercise to the routine

        Args:
            name_id: A string representing the html variable label for the name
                of the exercise
            sets_id: A string representing the html variable label for the
                number of sets for the exercise
        """
        exercise = Exercise(name_id, sets_id)
        self.exercises[exercise.name] = exercise

    def __repr__(self):
        return " ".join(
            [self.exercises[ex].__repr__() for ex in self.exercises]
        )
