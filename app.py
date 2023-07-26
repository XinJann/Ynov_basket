from flask import Flask, make_response, render_template, redirect, request
import flask
import uuid
import bcrypt
import mysql.connector
from flask_bcrypt import generate_password_hash, check_password_hash
from math import ceil

app = Flask(__name__)

database =""
user=""
password=""

with open('credentials.txt','r') as f:
    lines = f.readlines()
    database = lines[0].replace('\n','')
    user = lines[1].replace('\n','')
    password = lines[2].replace('\n','')

connection = mysql.connector.connect(host='localhost',
                                         database=database,
                                         user=user,
                                         password=password)
cursor = connection.cursor()

salt=bcrypt.gensalt()

cards_per_page = 100

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

def get_team_data_from_id(team_id):
    cursor.execute('SELECT * FROM teams WHERE team_id=%s', (team_id,))

def get_players_from_page(page_number,cards_per_page):
    cursor.execute('SELECT player_id,first_name, last_name FROM players LIMIT %s OFFSET %s', (cards_per_page,page_number*cards_per_page))
    return cursor.fetchall()

def get_teams_from_page(page_number,cards_per_page):
    cursor.execute('SELECT team_id,team_name FROM teams LIMIT %s OFFSET %s', (cards_per_page,page_number*cards_per_page))
    return cursor.fetchall()

def get_games_from_page(page_number,cards_per_page):
    cursor.execute("""
SELECT game_id,attack.abbreviation,defense.abbreviation,game_date FROM games 
JOIN teams as attack ON home_team_id = attack.team_id
JOIN teams as defense ON visitor_team_id = defense.team_id
LIMIT %s OFFSET %s;
""", (cards_per_page,page_number*cards_per_page))
    return cursor.fetchall()

def sanitize_current_page(page):
    if page:
        current_page = int(page)
        if current_page <= 0:
            current_page = 1
    else:
        current_page = 1
    return current_page

def get_total_pages(table):
    if table == "games":
        cursor.execute('SELECT COUNT(*) FROM games')
        return cursor.fetchone()[0]
    elif table == "players":
        cursor.execute('SELECT COUNT(*) FROM players')
        return cursor.fetchone()[0]
    elif table == "teams":
        cursor.execute('SELECT COUNT(*) FROM teams')
        return cursor.fetchone()[0]

    
@app.route('/', methods=['GET'])
def players():
    session_id = flask.request.cookies.get('session_id')
    
    current_page = sanitize_current_page(request.args.get("page"))
    total_pages = ceil(get_total_pages("players")/cards_per_page)
    if current_page > total_pages:
        current_page = total_pages
    
    datas = get_players_from_page(current_page-1,cards_per_page)
    return render_template('players.html', players = datas, current_page = current_page, total_pages = total_pages)

@app.route('/teams', methods=['GET'])
def teams():
    session_id = flask.request.cookies.get('session_id')
    
    current_page = sanitize_current_page(request.args.get("page"))
    total_pages = ceil(get_total_pages("teams")/cards_per_page)
    if current_page > total_pages:
        current_page = total_pages
    
    datas = get_teams_from_page(current_page-1,cards_per_page)
    return render_template('teams.html', teams = datas, current_page = current_page, total_pages = total_pages)

@app.route('/games', methods=['GET'])
def games():
    session_id = flask.request.cookies.get('session_id')

    current_page = sanitize_current_page(request.args.get("page"))
    total_pages = ceil(get_total_pages("games")/cards_per_page)
    if current_page > total_pages:
        current_page = total_pages
    
    datas = get_games_from_page(current_page-1,cards_per_page)
    return render_template('games.html', games = datas,current_page = current_page, total_pages = total_pages)

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