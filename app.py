from flask import url_for, Flask, render_template, request, redirect
from modules import plan

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/plan")
def plan_page():
    routines.append(plan.Routine())
    return render_template("plan.html")


@app.route("/addexercise")
def submit_exercise():
    routines[-1].add_exercise("exercise-name", "sets")
    for r in routines:
        print(r)
    return redirect(url_for("plan_page"))


@app.route("/submitroutine")
def submit_routine():
    pass


if __name__ == "__main__":
    routines = []
    app.run(debug=True)
