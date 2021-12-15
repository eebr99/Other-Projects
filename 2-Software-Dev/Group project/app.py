
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re
from flask_bootstrap import Bootstrap



# Initialize
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'Flask%Crud#Application'

# Enter your database connection details below

conn = sqlite3.connect('CRUDdb.sqlite', check_same_thread=False)

'''
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = "localhost"
app.config['MYSQL_DATABASE_PORT'] = 3308
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flaskcrud'
'''

'''
USers:
User: John12 Password: John1234
User: Tina11 Password: efgh1234 
'''

# Intialize MySQL
# mysql.init_app(app)


@app.route('/')
def main():
    return render_template('about.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/loggin')
def loggin():
    return render_template('loggin.html')


@app.route('/rating')
def rating():
    return render_template('rating.html')


@app.route('/payment')
def payment():
    return render_template('payment.html')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html')

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if user exists using MySQL
        # conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        # Fetch one record and return result
        user = cursor.fetchone()
        print(user)
        # If user exists in users table in out database
        if user and check_password_hash(user[4], password):
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            # Redirect to home page
            return render_template('index.html')
        else:
            # user doesnt exist or username/password incorrect
            msg = "Incorrect username or password"

    # Show the login form with message (if any)
    return render_template('loggin.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        last = request.form['last_name']
        first = request.form['first_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        hash = generate_password_hash(password)

        # Check if user exists using MySQL
        # conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        # If user exists show error and validation checks
        if user:
            msg = 'Username/user already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # user doesnt exists and the form data is valid, now insert new user into users table
            cursor.execute('INSERT INTO users (firstname, lastname, email, username, password) VALUES (?, ?, ?, ?, ?)',
                           (first, last, email, username, hash,))
            conn.commit()
            msg = 'You have successfully registered!'
            return render_template('loggin.html')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


if __name__ == "__main__":
    app.run()
