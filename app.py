from flask import Flask, make_response, render_template, redirect
import flask
import uuid
import bcrypt
import mysql.connector
from flask_bcrypt import generate_password_hash, check_password_hash

# add theses parameters in curl command to return the response time
# -w %{time_total} -o /dev/null

# Payload qui bypass le test
# curl --cookie "session_id=57177389-7cb7-4c37-a8dd-e2913639b07e' OR 1=1 Limit 1#" localhost:5000/admin


app = Flask(__name__)

connection = mysql.connector.connect(host='localhost',
                                         database='',
                                         user='',
                                         password='')
cursor = connection.cursor()

salt=bcrypt.gensalt()
# Create users table if it doesn't exist

#with open('script.sql', 'r') as sql_file:
    #connection.executescript(sql_file.read())

def executeScriptsFromFile(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        if command.strip() != '':
            cursor.execute(command)

# executeScriptsFromFile('script.sql')

def get_cookie_from_user(user_id):
    cursor.execute('SELECT cookie FROM users WHERE id=%s', (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def get_user_from_cookie(cookie):
    cursor.execute('SELECT username FROM users WHERE cookie=%s', (cookie,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

# Function to set a cookie for a user
def set_cookie(cookie):
    response = make_response(redirect('/'))
    response.set_cookie('session_id', cookie)
    return response


# Index page
@app.route('/', methods=['GET'])
def index():
    session_id = flask.request.cookies.get('session_id')
    print(session_id)
    # return render_template('index.html', result = admin_check(session_id), logged = session_id)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the user is already logged in
    if flask.request.method == 'GET':
        session_id = flask.request.cookies.get('session_id')
        user = get_user_from_cookie(session_id)
        print(session_id)
        if user != None:
            return 'You are already logged in. <a href="/">Go to the home page</a>'
        else:
            return render_template('login.html')
    else:
        username = flask.request.form['username']
        password = flask.request.form['password']
        cursor.execute('SELECT id, password FROM users WHERE username=%s', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            return set_cookie(get_cookie_from_user(user[0]))
        else:
            return 'Invalid username or password'

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
        session_id = flask.request.cookies.get('session_id')
        user = get_user_from_cookie(session_id)
        print(session_id)
        if user != None:
            return 'You are already logged in. <a href="/"> Go to the home page</a>'
        else:
            return render_template('register.html')
        # return render_template('register.html')
    else:
        username = flask.request.form['username']
        password = flask.request.form['password']
        cursor.execute('SELECT id FROM users WHERE username=%s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return 'Username already taken'
        else:
            cookie = str(uuid.uuid4())
            hashed_password = generate_password_hash(password).decode('utf-8')
            # password=bcrypt.hashpw(password.encode('utf-8'),salt)
            cursor.execute('INSERT INTO users (username, password, cookie) VALUES (%s, %s, %s)', (username, hashed_password, cookie))
            connection.commit()

            return set_cookie(cookie)

@app.route('/logout', methods=['GET'])
def logout():
    res = make_response(redirect('/'))
    res.set_cookie('session_id', 'bar', max_age=0)
    return res

if __name__ == '__main__':
    app.run()