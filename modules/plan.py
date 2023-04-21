from flask import request


class Exercise:
    def __init__(self, name_id, sets_id):
        self.name = request.args.get(name_id)
        self.sets = request.args.get(sets_id)

    def __repr__(self):
        return f"{self.name}, {self.sets}"


class Routine:
    def __init__(self, name_id):
        self.exercises = []
        self.name = request.args.get(name_id)

    def add_exercise(self, name_id, sets_id):
        self.exercises.append(Exercise(name_id, sets_id))

    def __repr__(self):
        return " ".join([ex.__repr__() for ex in self.exercises])
