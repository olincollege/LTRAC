"""
LTRAC viewer
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """
    Displays home.html in a web page
    """
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
