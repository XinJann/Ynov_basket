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

strings_to_sign = {"gt" : ">", "gte" : ">=", "eq" : "=", "lte" : "<=", "lt" : "<"}

strings_to_sign = {"gt" : ">=", "gte" : ">=", "eq" : "=", "lte" : "<=", "lt" : "<"}

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

def build_filter_query_for_players(player : str,position,height,height_sign,weight,weight_sign,sort_type,page_number):
    query="SELECT player_id,first_name, last_name FROM players"
    original_query = query + " WHERE"
    parameters = []
    arbitre=True
    if player:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        parameters.append("%" + player.capitalize() + "%")
        parameters.append("%" + player.lower() + "%")
        query = query + " (first_name LIKE %s OR last_name LIKE %s)"
    if height:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if height_sign in strings_to_sign:
            if query == original_query:
                query = query + " (feet * 0.3048) + (inches * 0.0254) " + strings_to_sign[height_sign] + " %s"
            else:
                query = query + " AND (height_feet * 0.3048) + (height_inches * 0.0254) " + strings_to_sign[height_sign] + " %s"
            parameters.append(height)
        else:
            return "ERROR"
    if weight:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if weight_sign in strings_to_sign:
            if query == original_query:
                query = query + " weight_pounds " + strings_to_sign[weight_sign] + " %s"
            else:
                query = query + " AND weight_pounds " + strings_to_sign[weight_sign] + " %s"
            parameters.append(round(float(weight) * 2.20462))
        else:
            return "ERROR"
    if position:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if query == original_query:
            query = query + " position LIKE %s"
        else:
            query = query + " AND position LIKE %s"
        parameters.append("%" + position + "%")
    if sort_type:
        if sort_type == "alphabetical":
            query = query + " ORDER BY first_name,last_name"
        elif sort_type == "height":
            query = query + " ORDER BY height_feet,height_inches"
        elif sort_type == "weight":
            query = query + " ORDER BY weight_pounds"
    #query = query + " LIMIT %s OFFSET %s"
    #parameters.append(cards_per_page)
    #parameters.append(int(page_number)*cards_per_page)
    return [query,parameters]

@app.route('/', methods=['POST','GET'])
def players():
    session_id = flask.request.cookies.get('session_id')

    if request.method == 'POST':
        player = request.form['playerName']
        position = request.form['playerPosition']
        height = request.form['playerHeight']
        height_sign = request.form['height_sign']
        weight = request.form['playerWeight']
        weight_sign = request.form['weight_sign']
        sort_type = request.form['sortingOption']
        page_number = sanitize_current_page(request.form['page'])

        if not player and not position and not height and not weight :
            return redirect('/')
        
        parameters_wraped = [player,height,height_sign,weight,weight_sign,position,sort_type]

        query_parameters = build_filter_query_for_players(player,position,height,height_sign,weight,weight_sign,sort_type,page_number-1)
        cursor.execute(query_parameters[0],query_parameters[1])
        datas = cursor.fetchall()
        total_pages=ceil(len(datas)/cards_per_page)
        datas = datas[(page_number-1)*cards_per_page:page_number*cards_per_page]

        return render_template('players.html', players = datas, current_page = page_number, total_pages = total_pages, post = True,parameters = parameters_wraped)
    
    elif request.method == 'GET':
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