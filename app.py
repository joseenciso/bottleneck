import os
import uuid
import base64
import bson
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
    return render_template(
        "index.html",
        posts=mongo.db.posts.find()
        )


@app.route('/gallery/<filename>')
def gallery(filename):
    # reponse = mongo.send_file(filename)
    # import pdb;pdb.set_trace()
    # return reponse
    return mongo.send_file(filename)


@app.route('/review')
def game_review():
    review = mongo.db.posts
    # review.
    # return render_template("reviews.html")
    post_cover=mongo.send_file(filename)
    return render_template('reviews.html', review=review, covers=post_cover)


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
                            "post_cover": post_cover.filename,
                            "posted_by": session["username"],
                            "post_review": request.form["post-review"],
                            "pros_content": request.form["post-pros"],
                            "cons_content": request.form["post-cons"]
                        }
                    )
            ###########################################
            # posting = mongo.db.posts
            # users = mongo.db.user

            # post_cover = request.files["post-cover"]
            # # gallery_1 = request.files["gallery-1"]
            # # gallery_2 = request.files["gallery-2"]
            # # gallery_3 = request.files["gallery-3"]
            # # gallery_4 = request.files["gallery-4"]
            # # gallery_5 = request.files["gallery-5"]

            # mongo.save_file(post_cover.filename, post_cover)

            # posting.insert(
            #     {
            # #         "post_title": request.form["post-title"],
            # #         "post_subtitle": request.form["release-date"],
            # #         "date_released": request.form["release-date"],
            #         "post_cover": request.files["post-cover"],
            # #         "post_cover": post_cover,
            # #         "post_cover_link": request.form["post-cover-link"],
            # #         "date_posted": datetime.now(),
            # #         "post_review": request.form["post-review"],
            # #         "pros_content": request.form["post-pros"],
            # #         "cons_content": request.form["post-cons"],
            # #         # "gallery_1": request.form[""],
            # #         # "gallery_2": request.form[""],
            # #         # "gallery_3": request.form[""],
            # #         # "gallery_4": request.form[""],
            # #         # "gallery_5": request.form[""],
            # #         "posted_by": session["username"]
            #     }
            # )




        # if "post_cover" in request.files:
        #     post_cover = request.files["post-cover"]
        #     posting.save(post_cover.filename, post_cover)
        #     posting.insert_one({"post_cover": post_cover.filename})

        # if "gallery_1" in request.files:
        #     gallery_1 = request.files["gallery_1"]
        #     gallery_1.save(gallery_1.filename, gallery_1)
        #     posting.insert_one({"gallery_1": gallery_1.filename})

        # if "gallery_2" in request.files:
        #     gallery_2 = request.files["gallery_2"]
        #     gallery_2.save(gallery_2.filename, gallery_2)
        #     posting.insert_one({"gallery_2": gallery_2.filename})

        # if "gallery_3" in request.files:
        #     gallery_3 = request.files["gallery_3"]
        #     gallery_3.save(gallery_3.filename, gallery_3)
        #     posting.insert_one({"gallery_3": gallery_3.filename})

        # users = mongo.db.user
        # users.find_one({
        #         "username": session["username"]
        #         })
        # user.insert_one({"posts": posting})
        # session["posts"]
        return redirect(url_for("index"))
    return render_template("post.html")


@app.route('/edit_post/<post_id>')
def edit_post(post_id):
    posts = mongo.db.posts.find_one(
            {
                "_id": ObjectId(post_id)
            }
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
