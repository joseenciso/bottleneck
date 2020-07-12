import os
import uuid
import base64
import bson
import gridfs
# from bottle import response
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
@app.route('/home')
def index():
    posts = mongo.db.posts.find()
    return render_template("index.html", posts=posts)



@app.route("/uploads/<filename>", methods=['GET'])
def upload(filename):
    return mongo.send_file(filename)


@app.route('/review/<review_name>')
def game_review(review_name):
    review = mongo.db.posts.find_one_or_404({'post_title': review_name})
#     # covers=post_cover
#     # review.
#     # return render_template("reviews.html")
#     # post_cover=mongo.send_file(cover)
    return render_template('reviews.html', post=review)


@app.route('/post', methods=['GET', 'POST'])
# @login_required
def post_review():
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        if request.files:

            # post_cover = request.files["post-cover"]
            #######################################
            if "post-cover" in request.files:
                post_cover = request.files["post-cover"]
                # posting = mongo.db.posts
                # users = mongo.db.user
                mongo.save_file(post_cover.filename, post_cover)
                mongo.db.posts.insert(
                        {
                            "post_title": request.form["post-title"],
                            "post_subtitle": request.form["post-subtitle"],
                            "post_cover": post_cover.filename,
                            "posted_by": session["username"],
                            "post_review": request.form["post-review"],
                            "pros_content": request.form["post-pros"],
                            "cons_content": request.form["post-cons"],
                            "date_posted": datetime.now(),
                        }
                    )
            ###########################################

        return redirect(url_for("index"))
    return render_template("post.html")


@app.route('/edit_post/<post_title>')
def edit_post(post_title):
    posts = mongo.db.posts.find_one(
            {"post_title": post_title}
        )


@app.route('/login', methods=["GET", "POST"])
def login():
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        user = mongo.db.users.find_one(
            {"username": request.form["username"].lower()}
            # {'email': request.form['email']}
        )
        if user:
            if bcrypt.hashpw(request.form["password"].encode("utf-8"),
                             user["password"]) == user["password"]:
                session["username"] = request.form["username"]
                # username = session.get["username"]
                return redirect(url_for("index"))
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("_id", None)
    session.clear()
    return redirect(url_for("login"))


@app.route('/user')
# @login_required
def user():
    # import pdb;pdb.set_trace()
    # user = g.get("user")
    if "username" in session:
        user = session["username"]
        # session.pop('user_id', None)
        return render_template('user.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        find_user = users.find_one(
            {'username': request.form['username'].lower()},
            # {'email': request.form['email']}
        )
        if find_user is None:
            # Encoding the password to UTF-8 in order to hash it
            hash_password = bcrypt.hashpw(
                request.form['password'].encode('utf-8'),
                bcrypt.gensalt()
            )
            # Inserting a new user
            users.insert_one(
                {
                    'username': request.form['username'].lower(),
                    'email': request.form['email'],
                    'password': hash_password,
                    'posts': []
                }
            )
            return redirect(url_for('index'))
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
