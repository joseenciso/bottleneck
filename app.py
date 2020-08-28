import os
import bcrypt
from flask import (
    Flask, render_template, redirect, url_for,
    request, session, flash, jsonify
)
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from datetime import datetime 
from flask_pymongo import PyMongo
# from flask_paginate import Pagination, get_page_args
# from flask_mongoengine import MongoEngine
import click
#from mongonator import MongoClientWithPagination, ASCENDING


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
        'Nintendo Switch','Nintendo Wii', 'Nintendo Wii U', 'Nintendo 3DS',
        'XBOX 360', 'XBOX ONE', 'PS2', 'PS3', 'PS4',
        'Linux', 'Mac', 'Windows'
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
@app.route('/home')
def index():
    # post  = mongo.db.posts
    # offset = int(request.args['offset'])
    # limit = int(request.args['limit'])
    # 
    # offset = 2
    #limit = 2
    # 
    # initial_post = post.find().sort('_id', -1)
    # last_post = initial_post[offset]['_id']
    # pages = post.find({'_id': {'$lte': last_post}}).sort('_id', -1).limit(limit)
    # output = []
    # 
    # for i in pages:
    #     output.append(i['_id'])
    #     print(output)
    # 
    # next_url = '?limit=' + str(limit) + '&offset=' + str(offset + limit)
    # prev_url = '?limit=' + str(limit) + '&offset=' + str(offset - limit)
    # 
    # return jsonify({'result': output, 'prev_url': prev_url, 'next_url': next_url})
    #return jsonify({'result': output, 'prev_url': '', 'next_url': ''})
    # page=n
    # posts = mongo.db.posts.find().sort('date_posted', -1).limit(5)
    # posts = mongo.db.posts.find().sort('_id', pymongo.ASCENDING)
    # pages = mongo.query.paginate(per_page=5)
    # next = mongo.db.posts.find().sort('date_posted', -1).skip(5).limit(5)
    posts = mongo.db.posts.find().sort('date_posted', -1)
    return render_template("index.html", posts=posts)
    #return render_template("index.html", post=output, next_url=next_url, prev_url=prev_url)
    


@app.route("/uploads/<filename>", methods=['GET'])
def upload(filename):
    return mongo.send_file(filename)


@app.route('/review/<review_id>')
def game_review(review_id):
    post = mongo.db.posts.find_one({'_id': ObjectId(review_id)})
    # release_date = post.release_date.strftime('%d/%b/%Y')
    # covers=post_cover
    # review.
    # return render_template("reviews.html")
    # post_cover=mongo.send_file(cover)
    #if post.game_score >= 50:
    #    score = '<div class="progress-circle over50 p{{post.game_score}}">'
    #else:
    #    score = '<div class="progress-circle first50-bar p{{post.game_score}}">'
    #fifty = 50
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
                # post_array = mongo.db.users.update({'username': session["session"]},
                #    {"$push": {"post_title": request.form["post-title"],
                #                "post_subtitle": request.form["post-subtitle"],} })

            ###########################################

        return redirect(url_for("index"))
    return render_template("post.html", platforms=platforms, pegi_desc=pegi_description, pegi_rate=pegi_rate)


@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if "username" in session:
        # post = mongo.db.posts.find_one(
        #         {"post_title": post_id}
        #     )
        # , edit_post=mongo.db.posts.find({"post_title": post_title})
        post = mongo.db.posts.find_one(
                        {"_id": ObjectId(post_id)})
        # release_date = post.release_date.datetime.strptime( '%Y-%m-%d')
        # return render_template("edit_post.html",
        #                         post=post,
        #                         release_date=release_date)
        return render_template("edit_post.html",
                                post=post,
                                platforms=platforms,
                                pegi_description=pegi_description,
                                pegi_rate=pegi_rate)
    else:
        session.pop("_id", None)
        return redirect(url_for('login'))


@app.route('/update_post/<post_id>', methods=['POST'])
def update_post(post_id):
    #import pdb;pdb.set_trace()
    gallery = {}
    for key, value in request.files.items():
        if value.filename != "":
            gallery.update({key: value.filename})
            mongo.save_file(value.filename, value)
    release_date = datetime.strptime(request.form["release-date"], '%Y-%m-%d')
    gallery.updateOne( {"$set": {
                "post_title": request.form["post-title"],
                "post_subtitle": request.form["post-subtitle"],
                "release_date": release_date,
                "date_edited": datetime.now(),
                "no_players": request.form["no_players"],
                "game_score": request.form["game_score"],
                "game_platform": request.form.getlist("platforms"),
                "pegi_desc": request.form.getlist("pegi-desc"),
                "pegi_rate": request.form["pegi-rate"],
                "pegi_rate": request.form["pegi-rate"],
                "pros_content": request.form["post-pros"],
                "cons_content": request.form["post-cons"],
                "post_review": request.form["post-review"],
                }})
    mongo.db.posts.update({"_id": ObjectId(post_id)}, gallery)
    return redirect(url_for('index'))


@app.route('/delete_post/<post_id>')
def delete_post(post_id):
    post = mongo.db.posts.find_one({"_id": post_id})
    print(post)
    return redirect(url_for('index'))


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
        username = session["username"]
        user = mongo.db.users.find_one({"username": username})
        # session.pop('user_id', None)
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
