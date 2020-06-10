import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from datetime import timedelta

username = os.getenv('C9_USER')

# Connnect to DB
# connection = pymysql.connect(host='localhost', user=username, password='', db='review_post')

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
# app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bootleneck.db'
# Relative path for the current path
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    # Linking witht the Post Model - Lazy=True SQL will load the date in one go

    def __repr__(self):
    # REPR Method or magic methods|Speficies how a method will be printed out
        return f"User('{self.username}', '{self.email}', '{self.profile_image}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(60), nullable=False)
    post_subtitle = db.Column(db.String(100))
    date_released = db.Column(db.DateTime, nullable=False, default=datetime)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    pros_content = db.Column(db.Text, nullable=False)
    cons_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def _repr__(self):
    # REPR Method or magic methods|Speficy's how a method will be printed out
        return f"Post('{self.post_title}', '{self.post_subtitle}', '{self.date_released}', '{self.date_posted}')"



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
        session.pop('id', None)
        # None when no returning anything
        username = request.form["username"]
        password = request.form['password']

        user = User(username=username, password=password)
        # Serch for te username
        # Checking wether password is right or not
        if user:
            session['id'] = user.id
            # g['user'] = user
            flash("Welcome {username}")
            return redirect(url_for('user'))

        flash("Wrong username or password")
        return redirect(url_for('login'))
    # flash("You ave been logged out 2")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("id", None)
    flash("Yo have been logged out!", "info")
    # Flash message, "category"
    return redirect(url_for("login"))


@app.route('/user')
def user():
    # import pdb;pdb.set_trace()
    # user = g.get("user")
    if not user:
        # session.pop('user_id', None)
        return redirect(url_for('login'))
    return render_template('user.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User(username=username, email=email, password=password)

        db.session.add(user)
        db.session.commit()
    return render_template("register.html")


@app.route('/contact_us')
def contact_us():
    return render_template("contactus.html")


if __name__ == "__main__":
    app.run(host=os.getenv('IP', "0.0.0.0"), port=int(os.getenv('PORT', "8080")), debug=True)
