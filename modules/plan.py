from flask import request


class Exercise:
    def __init__(self, name_id, sets_id):
        self.name = request.args.get(name_id)
        self.sets = request.args.get(sets_id)


class Routine:
    def __init__(self):
        self.exercises = []

    def add_exercise(self, name_id, sets_id):
        self.exercises.append(Exercise(name_id, sets_id))
