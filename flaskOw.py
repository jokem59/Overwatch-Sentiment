from flaskext.mysql import MySQL
import ConfigParser
from flask import Flask, render_template, flash, redirect
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

mysql = MySQL()
app = Flask(__name__)
app.config.from_object('config')

config = ConfigParser.ConfigParser()
config.read('/Users/JoeK/config_files/owconfig')

db_user = config.get('mysql', 'db_user')
db_pword = config.get('mysql', 'db_pword')
db_name = config.get('mysql', 'db_name')
db_host = config.get('mysql', 'db_host')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(db_user, db_pword, db_host, db_name)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

db = SQLAlchemy(app)

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    sentiment = db.Column(db.Float)
    subjectivity = db.Column(db.Float)
    text = db.Column(db.String)

    def __init__(self, date, time, sentiment, subjectivity, text):
        self.date = date
        self.time = time
        self.sentiment = sentiment
        self.subjectivity = subjectivity
        self.text = text

    def __repr__(self):
        return 'Tweet sentiment: {}'.format(self.sentiment)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String)
    join_date = db.Column(db.Date)

    def __init__(self, userid, join_date):
        self.userid = userid
        self.join_date = join_date

    def __repr__(self):
        return 'User: {}'.format(self.userid)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template("index.html")

@app.route('/query')
def get_tweets():
    return render_template('query.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

if __name__ == "__main__":
    # starts the website on a server
    app.run(debug=True)