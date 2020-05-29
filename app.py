import os
# import json
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/review')
def game_review():
    return render_template("reviews.html")


@app.route('/post')
def post_game_review():
    return render_template("post.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/contact_us')
def contact_us():
    return render_template("contactus.html")


if __name__ == "__main__":
    app.run(host=os.getenv('IP', "0.0.0.0"), port=int(os.getenv('PORT', "8080")),debug=True)
