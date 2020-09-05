import os
import bcrypt
import click
import math
from flask import (
    Flask, render_template, redirect, url_for,
    request, session, flash, jsonify
)
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from datetime import datetime 
from flask_pymongo import PyMongo
from werkzeug.exceptions import HTTPException


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


platforms = [
        'Switch','Wii', 'Wii U', '3DS',
        'XBOX 360', 'XBOX ONE', 'PS2', 'PS3', 'PS4',
        'Linux', 'Mac', 'Windows', 'iOS'
        ]

pegi_description = {
        'pegi-language': 'Bad Language',
        'pegi-discrimination': 'Discrimination',
        'pegi-drugs': 'Drugs',
        'pegi-fear': 'Fear',
        'pegi-gambling': 'Gambling',
        'pegi-purchase': 'In-Game Purchase',
        'pegi-sex': 'Sexual Content',
        'pegi-violence': 'Violence'
}

pegi_rate = ['pegi3', 'pegi7', 'pegi12', 'pegi16', 'pegi18']


def mongo_connect(url):
    try:
        connection = PyMongo.MongoClient(url)
        print("Connected!")
        return connection
    except PyMongo.errors.ConnectionFailure as e:
        print("Couldnt connect to MongoDB: %s") % e


encrypt = bcrypt.gensalt()


@app.route('/')
@app.route('/index')
def home():
    return redirect(url_for('index', page=1))


@app.route('/home')
def index():
    post = mongo.db.posts
    
    page = int(request.args['page'])
    
    offset = 0
    limit = 4

    number = post.count()
    pages = math.ceil(number/limit)

    prev_url = page-1
    next_url = page+1
    
    if page >= pages:
        next_url = pages
    elif page <= 1:
        prev_url = 1
        page = 1

    if page <= 1:
        offset = 0
        page=1
    elif page == 2:
        offset = 4
    elif page == 3:
        #page = pages
        offset = prev_url*4
    
    all_posts = post.find().sort('_id', -1)
    offset_post = post.find().sort('_id', -1).skip(offset).limit(limit)
    
    all_titles = []
    titles = []
    #import pdb;pdb.set_trace()
    posts = post.find().sort('_id', -1)
    for i in all_posts:
        all_titles.append(i['post_title'])
    
    for i in posts:
        titles.append(i['post_title'])

    # import pdb;pdb.set_trace()
    return render_template('index.html', posts=offset_post, page=page, pages=pages, prev_url=prev_url, next_url=next_url)


@app.route("/uploads/<filename>", methods=['GET'])
def upload(filename):
    return mongo.send_file(filename)


@app.route('/review/<review_id>', methods=['GET'])
def game_review(review_id):
    post = mongo.db.posts.find_one({'_id': ObjectId(review_id)})
    return render_template('reviews.html', post=post)


@app.route('/post', methods=['GET', 'POST'])
def post_review():
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        if request.files:
            post_cover = request.files["post_cover"]
            gallery_1 = request.files["gallery_1"]
            gallery_2 = request.files["gallery_2"]
            gallery_3 = request.files["gallery_3"]
            gallery_4 = request.files["gallery_4"]
            gallery_5 = request.files["gallery_5"]
            release_date = datetime.strptime(request.form["release-date"], '%Y-%m-%d')
            mongo.save_file(post_cover.filename, post_cover)
            mongo.save_file(gallery_1.filename, gallery_1)
            mongo.save_file(gallery_2.filename, gallery_2)
            mongo.save_file(gallery_3.filename, gallery_3)
            mongo.save_file(gallery_4.filename, gallery_4)
            mongo.save_file(gallery_5.filename, gallery_5)
            mongo.db.posts.insert({
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
                        "pegi_rate": request.form['pegi-rate'],
                        "gallery_1": gallery_1.filename,
                        "gallery_2": gallery_2.filename,
                        "gallery_3": gallery_3.filename,
                        "gallery_4": gallery_4.filename,
                        "gallery_5": gallery_5.filename,
                        "pros_content": request.form["post-pros"],
                        "cons_content": request.form["post-cons"],
                        "post_review": request.form["post-review"],
                    })
                
        return redirect(url_for("index", page=1))
    return render_template("post.html", platforms=platforms, pegi_desc=pegi_description, pegi_rate=pegi_rate)


@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if "username" in session:
        post = mongo.db.posts.find_one(
                        {"_id": ObjectId(post_id)})
        return render_template("edit_post.html",
                                post=post,
                                platforms=platforms,
                                pegi_description=pegi_description,
                                pegi_rate=pegi_rate)
    else:
        session.pop("_id", None)
        return redirect(url_for('login'))


@app.route('/update_post/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    # import pdb;pdb.set_trace()
    gallery = {}
    for key, value in request.files.items():
        if value.filename != "":
            gallery.update({key: value.filename})
            mongo.save_file(value.filename, value)
    # import pdb;pdb.set_trace()
    release_date = datetime.strptime(request.form["release_date"], "%Y-%m-%d")
    # print(request.form["release_date"])

    date_posted = datetime.strptime(request.form["date_posted"], "%Y-%m-%d")
    gallery.update({
                "post_title": request.form["post-title"],
                "post_subtitle": request.form["post-subtitle"],
                "release_date": release_date,
                "date_posted": date_posted,
                "date_edited": datetime.now(),
                "edited_by": session["username"],
                "posted_by": request.form["posted_by"],
                "no_players": request.form["no_players"],
                "game_score": request.form["game_score"],
                "game_platform": request.form.getlist("platforms"),
                "pegi_desc": request.form.getlist("pegi_description"),
                "pegi_rate": request.form.get("pegi_rate"),
                "pros_content": request.form["post-pros"],
                "cons_content": request.form["post-cons"],
                "post_review": request.form["post-review"],
                })
    mongo.db.posts.update({"_id": ObjectId(post_id)}, {'$set': gallery })
    return redirect(url_for('index', page=1))


@app.route('/delete_post/<post_id>', methods=['GET', 'DELETE'])
def delete_post(post_id):
    mongo.db.posts.find_one_and_delete({"_id": ObjectId(post_id)}) 
    # mongo.db.posts.delete_one({"_id":  ObjectId(post)})
    return redirect(url_for('index', page=1))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = mongo.db.users.find_one(
            {"username": request.form["username"].lower()}
        )
        if user:
            if bcrypt.hashpw(request.form["password"].encode("utf-8"),
                             user["password"]) == user["password"]:
                session["username"] = request.form["username"]
                return redirect(url_for("index", page=1))
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("_id", None)
    session.clear()
    return redirect(url_for("login"))


@app.route('/user')
def user():
    if "username" in session:
        username = session["username"]
        user = mongo.db.users.find_one({"username": username})
        posts = mongo.db.posts.find()
        return render_template('user.html', username=username, user=user, posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        find_user = users.find_one(
            {'username': request.form['username'].lower()},
        )
        if find_user is None:
            hash_password = bcrypt.hashpw(
                request.form['password'].encode('utf-8'),
                bcrypt.gensalt()
            )
            users.insert_one(
                {
                    'username': request.form['username'].lower(),
                    'email': request.form['email'],
                    'password': hash_password,
                    'posts': []
                }
            )
            return redirect(url_for('index', page=1))
        else:
            flash('Username or email already exists')
    return render_template("register.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def page_forbiden(error):
    return render_template('errors/403.html', error=error), 403


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("errors/500.html", e=e), 500


if __name__ == "__main__":
    app.run(host=os.getenv('IP', "0.0.0.0"),
            port=int(os.getenv('PORT', "8080")),
            debug=False)
