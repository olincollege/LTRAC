"""
website framework
"""
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
    display = [rout.to_html_display() for _, rout in routines.items()]
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
    Adds routine to Routine object
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


# ---------------------Logging-------------------- #


@app.route("/logs", methods=["GET", "POST"])
def logs_page():
    """
    Renders logging page, access user input if present
    """
    if request.method == "POST":
        for exercise in exercise_list:
            for sets in range(exercise[1]):
                current_exercise = exercise[0]
                print(
                    current_exercise, request.form[f"{current_exercise} {sets}"]
                )

    display = [rout.to_html_display() for _, rout in routines.items()]
    return render_template("logs.html", routines=display, length=len(display))


@app.route("/logs/<routine>")
def log_exercise(routine):
    """
    Renders page for user to enter weights for each exercise in a routine
    """

    return render_template(
        "routinelog.html", routine=routine, inputs=exercise_list
    )


if __name__ == "__main__":
    routines = {}
    exercise_list = [["Squats", 3], ["Deadlift", 4]]
    app.run(debug=True)
