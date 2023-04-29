"""
website framework
"""

from flask import url_for, Flask, render_template, request, redirect
from modules.plan import Exercise, Routine
from modules.profile import User
from modules.dates import Weekday

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


@app.route("/logs/<day>")
def logs_page(day):
    """
    Renders logging page
    """
    print(user.routines)
    return render_template(
        "logs.html", day=day, routines=user.routines, length=len(user.routines)
    )


@app.route("/logs/<day>/<routine>")
def log_exercise(day, routine):
    """
    Renders page for user to enter weights for each exercise in a routine
    """
    exercise_dict = user.routines[routine].exercises
    print(exercise_dict)
    return render_template(
        "routinelog.html", day=day, routine=routine, inputs=exercise_dict
    )


@app.route("/submit-log/<day>/<routine>", methods=["GET", "POST"])
def submit_log(routine, day):
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
        user.to_json()
        # Save to csv
        user.routines[routine].export_log(
            f"user_data/{username}/{routine}/{routine}.csv"
        )
    return redirect(url_for("logs_page", day=day))


# -------------------Calendar----------------------#
@app.route("/calendar")
def calendar():
    """
    Renders Calendar page
    """
    days = [
        day.name.capitalize()
        for day, y_n in user.workout_days.items()
        if y_n == 1
    ]
    return render_template("calendar.html", workout_days=days, length=len(days))


@app.route("/select-days")
def select_days():
    """
    Renders page where user selects workout days
    """

    return render_template("selectdays.html")


@app.route("/submit-days", methods=["GET", "POST"])
def submit_days():
    """
    Fetch user input from /select-days
    """
    if request.method == "POST":
        days = request.form.getlist("day")
        user.set_workout_days([Weekday[day] for day in days])
        user.to_json()
    return redirect(url_for("select_days"))


if __name__ == "__main__":
    username = "Grustler"
    try:
        user = User.load_user_data(username)
    except FileNotFoundError:
        user = User(username)
    print(user.__dict__)
    app.run(debug=True)
