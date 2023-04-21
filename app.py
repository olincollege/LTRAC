from flask import url_for, Flask, render_template, request, redirect
from modules import plan

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

    length = len(routines)
    return render_template("plan.html", routines=routines, length=length)


# ------------- New routine --------------------#


@app.route("/add-routine")
def new_routine():
    """
    Asks user for a routine name, then redirects them to /add-exercise
    """
    return render_template("addroutine.html")


# ------------- Add exercise to routine ------------- #


@app.route("/add-exercise")
def add_new_exercise():
    """
    Renders page for adding new exercise
    """
    routine_name = request.args.get("routine-name")
    return render_template("addexercise.html", routine_name=routine_name)


@app.route("/submit-exercise")
def submit_exercise():
    """
    Adds new exercise to routine
    Sends user back to add more exercises
    """

    return redirect(url_for("add_new_exercise"))


@app.route("/submit-routine")
def submit_routine():
    """
    Adds new routine to a list of routines
    """

    return redirect(url_for("plan_page"))


if __name__ == "__main__":
    routines = [
        {"Routine 1": ["Leg Press", "Squats", "Deadlift"]},
        {"Routine 2": ["Lat pull down", "Pull ups"]},
        {"Routine 3": ["Leg Press", "Squats"]},
        {"Routine 4": ["Leg Press", "Squats"]},
        {"Routine 5": ["Leg Press", "Squats"]},
        {"Routine 6": ["Leg Press", "Squats"]},
        {"Routine 7": ["Leg Press", "Squats"]},
    ]
    app.run(debug=True)
