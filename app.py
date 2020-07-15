import os
import bcrypt
from flask import (
    Flask, render_template, redirect, url_for,
    request, session, flash
)
from datetime import datetime, timedelta
# from bottle import response
# import uuid
# import base64
# import bson
# import gridfs
# from flask_login import (
#                     LoginManager, UserMixin, login_required,
#                     current_user, login_user
#                     )

from bson.objectid import ObjectId

from flask_pymongo import PyMongo



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


@app.route('/review/<review_id>')
def game_review(review_id):
    post = mongo.db.posts.find_one({'_id': ObjectId(review_id)})
    # release_date = post.release_date.strftime('%d/%b/%Y')
#     # covers=post_cover
#     # review.
#     # return render_template("reviews.html")
#     # post_cover=mongo.send_file(cover)
    return render_template('reviews.html', post=post)


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
                gallery_1 = request.files["gallery_1"]
                gallery_2 = request.files["gallery_2"]
                gallery_3 = request.files["gallery_3"]
                gallery_4 = request.files["gallery_4"]
                gallery_5 = request.files["gallery_5"]
                release_date = datetime.strptime(request.form["release-date"], '%Y-%m-%d')
                # posting = mongo.db.posts
                # users = mongo.db.user
                mongo.save_file(post_cover.filename, post_cover)
                mongo.save_file(gallery_1.filename, gallery_1)
                mongo.save_file(gallery_2.filename, gallery_2)
                mongo.save_file(gallery_3.filename, gallery_3)
                mongo.save_file(gallery_4.filename, gallery_4)
                mongo.save_file(gallery_5.filename, gallery_5)
                mongo.db.posts.insert(
                        {
                            "post_title": request.form["post-title"],
                            "post_subtitle": request.form["post-subtitle"],
                            "release_date": release_date,
                            "post_cover": post_cover.filename,
                            "posted_by": session["username"],
                            "date_posted": datetime.now(),
                            "no_players": request.form["no_players"],
                            "game_score": request.form["game_score"],
                            "game_platform": request.form.getlist("platform"),
                            "pegi_desc": request.form.getlist("pegi-desc"),
                            "gallery_1": gallery_1.filename,
                            "gallery_2": gallery_2.filename,
                            "gallery_3": gallery_3.filename,
                            "gallery_4": gallery_4.filename,
                            "gallery_5": gallery_5.filename,
                            "pros_content": request.form["post-pros"],
                            "cons_content": request.form["post-cons"],
                            "post_review": request.form["post-review"],
                        }
                    )
            ###########################################

        return redirect(url_for("index"))
    return render_template("post.html")


# @app.route('/edit_post/<post_title>')
# def edit_post(post_title):
#     post = mongo.db.posts.find_one(
#             {"post_title": post_title}
#         )
#     return render_template("edit_post.html", edit_post=mongo.db.posts.find({"post_title": post_title}))


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
