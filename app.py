import os
import uuid
from flask import (
                Flask, render_template, redirect, url_for,
                request, session, flash
                )

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
# from flask_login import (
#                     LoginManager, UserMixin, login_required,
#                     current_user, login_user
#                     )

from bson.objectid import ObjectId

# from werkzeug.security import generate_password_hash, check_password_hash

from flask_pymongo import PyMongo

import bcrypt

username = os.getenv('C9_USER')

# MONGO_URI = os.getenv('MONGO_URI')


app = Flask(__name__)
app.secret_key = "SECRET_KEY"

app.config["MONGO_URI"] = 'mongodb+srv://rootAccess:sP9eU2GAtnYugO53@posting-vndhj.mongodb.net/bottleneckdb?retryWrites=true&w=majority'
app.config["MONGO_DBNAME"] = 'bottleneckdb'  # Optional setting

# Creating a new instance of PyMongo
mongo = PyMongo(app)

DBS_NAME = "bottleneckdb"
COLECCTION_NAME = "posts"


def mongo_connect(url):
    try:
        connection = PyMongo.MongoClient(url)
        print("Connected!")
        return connection
    except PyMongo.errors.ConnectionFailure as e:
        print("Couldnt connect to MongoDB: %s") % e


# login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = 'login'
encrypt = bcrypt.gensalt()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", users=mongo.db.users.find())


@app.route('/review')
def game_review():
    return render_template("reviews.html")


@app.route('/post')
# @login_required
def post_review():
    return render_template("post.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session["username"] = request.form["username"]
        # logging_in = users.find_one({"username": request.form["username"]})
        # if logging_in = users
        # username = mongo.db.users.find()
    """
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        flash('You are logged in')
    if "username" in session:
        return render_template("user.html")
    else:
        if request.method == "POST":
            # session.permanent = True
            # session.pop('id', None)
            # None when no returning anything
            username = request.form["username"]
            password = request.form['password']
            user = User(username=username, password=password)
            # Serch for te username
            # Checking wether password is right or not
            # if user:
            #     session['id'] = user.id
            #     # g['user'] = user
            #     flash("Welcome {username}")
            #     return redirect(url_for('user'))
            return redirect(url_for("user"))
            # flash("Wrong username or password")
            # return redirect(url_for('login'))
        # flash("You ave been logged out 2")
        else:
            return render_template("login.html")
    return render_template("login.html")
    """


@app.route('/logout')
def logout():
    session.pop("_id", None)
    session.clear()
    # session.pop("username", None)
    # session.pop("password", None)
    # flash("Yo have been logged out!", "info")
    # Flash message, "category"
    return redirect(url_for("index"))


@app.route('/user')
# @login_required
def user():
    # import pdb;pdb.set_trace()
    # user = g.get("user")
    # if "user" in session:
    #     user = session["user"]
    #     # session.pop('user_id', None)
    #     return render_template('user.html')
    # else:
    #     return redirect(url_for('login'))
    return render_template('user.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        find_user = users.find[
                    {'username': request.form['username']},
                    {'email': request.form['email']}
                    ]
        if find_user is None:
            # Encoding the password to UTF-8 in order to hash it
            hash_password = bcrypt.hashpw(
                                request.form['password'].encode('utf-8'),
                                bcrypt.gensalt()
                                )
            # Inserting a new user
            users.insert_one(
                {'username': request.form['username'],
                    'email': request.form['email'],
                    'password': hash_password,
                    'posts': ''}
                                    )
            return render_template('login.html')
        else:
            flash('Username or email already exists')
    return render_template("register.html")


@app.route('/contact')
def contact():
    return render_template("contactus.html")


if __name__ == "__main__":
    app.run(host=os.getenv('IP', "0.0.0.0"),
            port=int(os.getenv('PORT', "8080")),
            debug=True)
