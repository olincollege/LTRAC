"""
website framework
"""

from flask import url_for, Flask, render_template, request, redirect
from modules.plan import Exercise, Routine
from modules.profile import User

app = Flask(__name__)

# --------Home Page ---------#
@app.route("/")
def home():
    """
    Renders home page
    """
    print(user.routines)
    return render_template("home.html")


# ---------Everything that is linked with the Plan page--------- #
@app.route("/plan")
def plan_page():
    """
    Renders page for viewing routines/add new routine
    """

    return render_template(
        "plan.html", routines=user.routines, length=len(user.routines)
    )


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
    # Get routine name from user input in webpage
    new_routine_name = request.args.get("routine-name")
    user.add_routine(Routine(new_routine_name))
    user.to_json()
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
    # Add new exercise entered by user in webpage
    user.routines[routine].add_exercise_from_input("exercise-name", "sets")
    # user.routines[routine].to_json(f"user_data/routines/{routine}.json")
    user.export_routines()
    return redirect(url_for("add_new_exercise", routine=routine))


# ---------------------Logging-------------------- #


@app.route("/logs")
def logs_page():
    """
    Renders logging page
    """
    print(user.routines)
    return render_template(
        "logs.html", routines=user.routines, length=len(user.routines)
    )


@app.route("/logs/<routine>")
def log_exercise(routine):
    """
    Renders page for user to enter weights for each exercise in a routine
    """
    exercise_dict = user.routines[routine].exercises
    print(exercise_dict)
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
            user.routines[routine].load_log(
                f"user_data/{username}/{routine}/{routine}.csv"
            )
        except FileNotFoundError:
            pass

        user.log_workout(routine_name=routine)
        # Save to csv
        user.routines[routine].export_log(
            f"user_data/{username}/{routine}/{routine}.csv"
        )
    return redirect(url_for("logs_page"))


if __name__ == "__main__":
    username = "Grustler"
    try:
        user = User.load_user_data(username)
    except FileNotFoundError:
        user = User(username)
    print(user.__dict__)
    app.run(debug=True)
