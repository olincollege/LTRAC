"""
website framework
"""

from flask import url_for, Flask, render_template, request, redirect, session
from pathlib import Path
from modules.plan import Exercise, Routine
from modules.profile import User
from modules.dates import Weekday

app = Flask(__name__)


# ----------Login Page-----------#
@app.route("/")
def login():
    """
    Login page
    """
    return render_template("login.html")


@app.route("/auth", methods=["POST"])
def authenticate():
    """
    Check if user exists in system, create new user if not found
    """
    username = request.form["username"]
    global user
    try:
        user = User.load_user_data(username)
    except FileNotFoundError:
        user = User(username)

    return redirect(url_for("home", name=user.name))


# --------Home Page ---------#
@app.route("/home")
def home():
    """
    Renders home page
    """

    return render_template("home.html", name=user.name)


# --------Profile Page---------#


@app.route("/profile")
def profile():
    """
    Renders profile page
    """

    pic_path = Path(f"static/img/{user.name}_profile_picture.jpg")
    if pic_path.is_file():
        profile_pic = f"img/{user.name}_profile_picture.jpg"
    else:
        profile_pic = "img/default_profile.jpg"

    return render_template(
        "profile.html",
        username=user.name,
        photo=profile_pic,
        level=user.level(),
    )


@app.route("/edit-profile")
def edit_profile():
    """
    Renders page where user can upload a profile picture
    """
    return render_template("editprofile.html")


@app.route("/upload-successful", methods=["POST"])
def photo_uploaded():
    """
    Uploads photo into system
    """
    uploaded_files = request.files["file"]
    uploaded_files.save(f"static/img/{user.name}_profile_picture.jpg")
    return redirect(url_for("profile"))


# @app.route("/username-changed", methods=["GET"])
# def username_changed():
#     """
#     Updates username to new username the user inputted
#     """
#     global username
#     username = request.args.get("new_username")
#     return redirect(url_for("profile"))

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
                f"user_data/{user.name}/{routine}/{routine}.csv"
            )
        except FileNotFoundError:
            pass

        user.log_workout(routine_name=routine)
        user.to_json()
        # Save to csv
        user.routines[routine].export_log(
            f"user_data/{user.name}/{routine}/{routine}.csv"
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
    return redirect(url_for("calendar"))


if __name__ == "__main__":
    app.run(debug=True)
