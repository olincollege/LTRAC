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
    routines.append(plan.Routine())
    return render_template("plan.html")


@app.route("/add-exercise")
def add_new_exercise():
    """
    Renders page for adding new exercise
    """
    return render_template("addexercise.html")


@app.route("/submit-exercise")
def submit_exercise():
    """
    Adds new exercise to routine
    Sends user back to add more exercises
    """
    routines[-1].add_exercise("exercise-name", "sets")
    return redirect(url_for("add_new_exercise"))


@app.route("/submit-routine")
def submit_routine():
    """
    Adds new routine to a list of routines
    """
    return redirect(url_for("plan_page"))


if __name__ == "__main__":
    routines = []
    app.run(debug=True)
