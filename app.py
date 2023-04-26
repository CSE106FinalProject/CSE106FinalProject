from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.secret_key = 'cse106projsecretkey'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    user_name = db.Column(db.String(25), nullable = False)
    user_pass = db.Column(db.String(25), nullable = False)

    def __repr__(self):
        return '<users %r>' % (self.user_id)

class topics(db.Model):
    topic_id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    topic_name = db.Column(db.String(25), nullable = False)

    def __repr__(self):
        return '<topics %r>' % (self.topic_id)

class posts(db.Model):
    post_id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    post_subject = db.Column(db.String(100), nullable = False)
    post_date = db.Column(db.DateTime, nullable = False)
    post_topic = db.Column(db.Integer, nullable = False)
    post_by = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return '<posts %r>' % (self.post_id)

class reply(db.Model):
    reply_id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    reply_content = db.Column(db.String(200), nullable = False)
    reply_date = db.Column(db.DateTime, nullable = False)
    reply_post = db.Column(db.Integer, nullable = False)
    reply_by = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return '<reply %r>' % (self.reply_id)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    username = request.form['Username']
    password = request.form['Pass']
    account = users(user_name=username, user_pass=password)
    if account:
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        msg = 'Logged in successfully !'
        return render_template('home.html', msg = msg)
    else:
        msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)