from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, text
import sqlite3
import json
import os


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.secret_key = 'cse106projsecretkey'
#db = SQLAlchemy(app)
loginData_engine = create_engine('sqlite:///loginData.db', echo = True)
loginData_meta = MetaData()
loginData = Table(
   'loginData', loginData_meta,
   Column('id', Integer, primary_key = True),
   Column('username', String),
   Column('password', Integer))

loginData_meta.create_all(loginData_engine)
"""""
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
    """""

@app.route('/', methods=['GET', 'POST'])
def home():
    # Sets the current user to be null, displays login page
    if request.method == 'GET':
        session['username'] = "null"
        return render_template('login.html')
    
@app.route('/login', methods = ['PASS'])
def loginFunction():
    if (request.method == 'PASS'):
        loginData_connection = loginData_engine.connect()

        # Takes in username and password from the log-in page and assigns them to username and password
        loginForm = request.data
        loginForm = loginForm.decode()
        loginForm = json.loads(loginForm)
        username = str(loginForm['username'])
        password = loginForm['password']
        print(password)
        #loginData_connection.close()
        # Finds password in the database (hashed) and assigns it to matchingPass
        #s = "INSERT INTO loginData (username, password) VALUES ('" + username + "', '" + str(password) + "')"
        #loginData_connection.execute(text(s))
        #loginData_connection.commit()

        loginData_connection = loginData_engine.connect()
        s = "SELECT password FROM loginData WHERE username='" + username + "'"
        result = loginData_connection.execute(text(s))
        matchingPass = str(result.fetchone())
        print(matchingPass)
        print("THIS IS THE HASHED:")
        print(password)
        print('XXXXXXXXX')
        loginData_connection.close()
        print("test")


        if (matchingPass == "None"):
            print("TEST FAIL")
            return "fail"

        # Found a password: converting to int and displaying
        matchingPass = matchingPass[1:-2]
        matchingPass = int(matchingPass)


        # If the password matches, the below is executed to login the user
        if (password == matchingPass):
            print("TEEEEST PASS")
            session['username'] = username
            return "correct"
        else:
            return "incorrect"

@app.route('/signup', methods = ['GET','PASS'])
def signup():
    if (request.method =='GET'):
        return render_template('signup.html')
    
    if (request.method == 'PASS'):
        loginData_connection = loginData_engine.connect()

        loginForm = request.data
        loginForm = loginForm.decode()
        loginForm = json.loads(loginForm)
        username = str(loginForm['username'])
        password = loginForm['password']
        password1 = loginForm['password1']
        print(password)
        if(password == password1):
            s = "INSERT INTO loginData (username, password) VALUES ('" + username + "', '" + str(password) + "')"
            loginData_connection.execute(text(s))
            loginData_connection.commit()
            return "correct"
        else:
            return "incorrect"
        


@app.route('/display', methods = ['GET'])
def displaySetter():
    if session.get('username') is not None:
        if (session['username'] != "null"):
            return render_template('home.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/home')
def homes():
    # Establish a connection to the database
    conn = sqlite3.connect('instance/example.sqlite')
    cur = conn.cursor()

    # Query all posts from the database
    posts_query = "SELECT * FROM posts"
    cur.execute(posts_query)
    posts = cur.fetchall()

    # Query all replies from the database
    replies_query = "SELECT * FROM reply"
    cur.execute(replies_query)
    replies = cur.fetchall()

    # Create a dictionary to store replies by post ID
    replies_dict = {}
    for reply in replies:
        post_id = reply[1]
        if post_id in replies_dict:
            replies_dict[post_id].append(reply)
        else:
            replies_dict[post_id] = [reply]

    # Close the database connection
    conn.close()

    # Render the home template with the posts and replies data
    return render_template('home.html', posts=posts, replies_dict=replies_dict)

@app.route('/post')
def post():
    # Sets the current user to be null, displays login page
        return render_template('post.html')

@app.route('/topic')
def topic():
    # Sets the current user to be null, displays login page
        if session.get('username') is not None:
            if (session['username'] != "null"):
                return render_template('topic.html')
        else:
            return render_template('login.html')

"""""        
@app.route('/signup')
def signup():
    # Sets the current user to be null, displays login page
            return render_template('signup.html')
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)