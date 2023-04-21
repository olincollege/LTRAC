from flask import url_for, Flask, render_template, request, redirect
from modules.plan import Exercise, Routine

app = Flask(__name__)

# --------Home Page ---------#
@app.route("/")
def home():
    """
    Renders home page
    """
    return render_template("home.html")


# ---------Everything that is linked with the Plan page--------- #
@app.route("/plan")
def plan_page():
    """
    Renders page for viewing routines/add new routine
    """
    print(routines)
    display = routines
    return render_template("plan.html", routines=display, length=len(display))


# ------------- New routine --------------------#


@app.route("/add-routine")
def new_routine():
    """
    Asks user for a routine name, then redirects them to /add-exercise
    """
    return render_template("addroutine.html")


@app.route("/submit-routine")
def submit_routine():
    """
    docs
    """
    new_routine_name = request.args.get("routine-name")
    routines[new_routine_name] = Routine(new_routine_name)
    return redirect(url_for("add_new_exercise", routine=new_routine_name))


# ------------- Add exercise to routine ------------- #


@app.route("/add-exercise/<routine>")
def add_new_exercise(routine):
    """
    Renders page for adding new exercise
    """
    return render_template("addexercise.html", routine_name=routine)


@app.route("/submit-exercise/<routine>")
def submit_exercise(routine):
    """
    Adds new exercise to routine
    Sends user back to add more exercises
    """
    routines[routine].add_exercise_from_input("exercise-name", "sets")
    return redirect(url_for("add_new_exercise", routine=routine))


if __name__ == "__main__":
    routines = {}
    routines2 = [
        {"Routine 1": ["Leg Press", "Squats", "Deadlift"]},
        {"Routine 2": ["Lat pull down", "Pull ups"]},
        {"Routine 3": ["Leg Press", "Squats"]},
        {"Routine 4": ["Leg Press", "Squats"]},
        {"Routine 5": ["Leg Press", "Squats"]},
        {"Routine 6": ["Leg Press", "Squats"]},
        {"Routine 7": ["Leg Press", "Squats"]},
    ]
    app.run(debug=True)
