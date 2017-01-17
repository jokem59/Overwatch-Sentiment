from flaskext.mysql import MySQL
import ConfigParser
from flask import Flask, render_template, flash, redirect
from forms import LoginForm

mysql = MySQL()
app = Flask(__name__)
app.config.from_object('config')

config = ConfigParser.ConfigParser()
config.read('/Users/JoeK/config_files/owconfig')

app.config['MYSQL_DATABASE_USER'] = config.get('mysql', 'db_user')
app.config['MYSQL_DATABASE_PASSWORD'] = config.get('mysql', 'db_pword')
app.config['MYSQL_DATABASE_DB'] = config.get('mysql', 'db_name')
app.config['MYSQL_DATABASE_HOST'] = config.get('mysql', 'db_host')
mysql.init_app(app)


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