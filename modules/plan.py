from flask import request


class Exercise:
    """
    A gym exercise with number of sets

    Attributes:
        name: A string representing the name of the routine
        sets: An integer representing the number of sets for the exercise
    """

    def __init__(self, name, sets):
        self.name = name
        self.sets = sets

    @classmethod
    def from_input(cls, name_id, sets_id):
        """
        Create exercise from user input through the website

        Args:
            name_id: A string representing the html variable label for the name
                of the exercise
            sets_id: A string representing the html variable label for the
                number of sets for the exercise

        Returns:
            An Exercise object with the name and sets
        """
        return cls(request.args.get(name_id), request.args.get(sets_id))

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
        self.exercises[exercise.name] = exercise

    def __repr__(self):
        return " ".join([ex.__repr__() for ex in self.exercises.items()])
