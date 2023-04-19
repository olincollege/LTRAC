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
    profile_pic = "img/profile_picture.jpg"
    return render_template(
        "profile.html", username=username, photo=profile_pic, level=level
    )


@app.route("/edit-profile")
def edit_profile():
    """
    Renders page where user can change username, upload a profile picture
    """
    return render_template("editprofile.html")


@app.route("/upload-successful", methods=["POST"])
def photo_uploaded():
    """
    Uploads photo into system
    """
    uploaded_files = request.files["file"]
    uploaded_files.save("static/img/profile_picture.jpg")
    return redirect(url_for("profile"))


@app.route("/username-changed", methods=["GET"])
def username_changed():
    """
    Updates username to new username the user inputted
    """
    global username
    username = request.args.get("new_username")
    return redirect(url_for("profile"))


if __name__ == "__main__":
    routines = []
    username = "Grustler"
    level = 1
    app.run(debug=True)
