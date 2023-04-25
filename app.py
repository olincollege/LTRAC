"""
website framework
"""
import os
from flask import url_for, Flask, render_template, request, redirect
from modules.plan import Exercise, Routine

app = Flask(__name__)

# --------Home Page ---------#
@app.route("/")
def home():
    """
    Renders home page
    """
    print(routines)
    return render_template("home.html")


# ---------Everything that is linked with the Plan page--------- #
@app.route("/plan")
def plan_page():
    """
    Renders page for viewing routines/add new routine
    """

    return render_template("plan.html", routines=routines, length=len(routines))


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
    routines[routine].to_json(f"user_data/routines/{routine}.json")
    return redirect(url_for("add_new_exercise", routine=routine))


# ---------------------Logging-------------------- #


@app.route("/logs")
def logs_page():
    """
    Renders logging page
    """
    return render_template("logs.html", routines=routines, length=len(routines))


@app.route("/logs/<routine>")
def log_exercise(routine):
    """
    Renders page for user to enter weights for each exercise in a routine
    """
    exercise_dict = routines[routine].exercises
    return render_template(
        "routinelog.html", routine=routine, inputs=exercise_dict
    )


@app.route("/submit-log/<routine>", methods=["GET", "POST"])
def submit_log(routine):
    """
    Submit weights user entered
    """

    if request.method == "POST":
        try:
            routines[routine].load_log(f"user_data/logs/{routine}.csv")
        except FileNotFoundError:
            pass

        for _, exercise in routines[routine].exercises.items():
            current_exercise = exercise.name
            weight_list = [
                request.form[f"{current_exercise} {i}"]
                for i in range(int(exercise.sets))
            ]
            # A list that contains weights, ex: [50,55,60]
            exercise.log_weights_today(weight_list)
            # Save to csv
        routines[routine].export_log(f"user_data/logs/{routine}.csv")
    return redirect(url_for("logs_page"))


if __name__ == "__main__":
    routines = {}
    directory = "user_data/routines/"
    for filename in os.listdir(directory):
        curr_routine = Routine.from_json(f"{directory}{filename}")
        routines[curr_routine.name] = curr_routine

    app.run(debug=True)
