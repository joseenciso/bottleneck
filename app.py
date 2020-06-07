import os
from flask_sqlalchemy import SQLAlchemy
# import json
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from datetime import timedelta

username = os.getenv('C9_USER')

# Connnect to DB
# connection = pymysql.connect(host='localhost', user=username, password='', db='review_post')

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.permanent_session_lifetime = timedelta(minutes=5)


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    # This representation is to see it working on the cmmd line
    def __repr__(self):
        return f'<User: {self.username}>'


# List - Global variable that represents all the users
users = []
users.append(User(id=1, username="jose", password="pass1"))
users.append(User(id=2, username="joe", password="pass2"))

# Printing all the current users
print(users[0].id, users[0].username, users[0].password)


@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/review')
def game_review():
    return render_template("reviews.html")


@app.route('/post')
def post_game_review():
    return render_template("post.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # session.permanent = True
        session.pop('user_id', None)
        # None when no returning anything
        username = request.form["username"]
        password = request.form['password']

        # Serch for te username
        user_name = [x for x in users if x.username == username][0]
        # Checking wether password is right or not
        if user_name and user_name.password == password:
            session['user_id'] = user_name.id

            """
            session["username"] = users
            flash("Welcome back {{user}}")
            """
            flash("Welcome back {username}")
            return redirect(url_for('user'))
        """
        else:
            if "user" in session:
                flash("Already in!", "info")
                return redirect(url_for("user"))
        """
        flash("Wrong username or password")
        return redirect(url_for('login'))
    # flash("You ave been logged out 2")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("user_id", None)
    flash("Yo have been logged out!", "info")
    # Flash message, "category"
    return redirect(url_for("login"))


@app.route('/user')
def user():
    """
    if "user" in session:
        user = session["username"]
        return render_template("user.html", user=user)
    else:
        flash("not logged in!", "info")
        return redirect(url_for("login"))
    """

    if not g.user:
        # session.pop('user_id', None)
        return redirect(url_for('login'))
    return render_template('user.html')


@app.route('/contact_us')
def contact_us():
    return render_template("contactus.html")


if __name__ == "__main__":
    app.run(host=os.getenv('IP', "0.0.0.0"), port=int(os.getenv('PORT', "8080")), debug=True)
