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


# ---------Profile Page ---------------#
@app.route("/profile")
def profile():
    """
    Renders profile page
    """
    return render_template("profile.html")


@app.route("/edit-profile")
def edit_profile():
    """
    Renders page where user can change username, upload a profile picture
    """
    pass


@app.route("/upload-successful")
def photo_uploaded():
    """
    Uploads photo into system
    """
    pass


if __name__ == "__main__":
    routines = []
    app.run(debug=True)
