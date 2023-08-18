from flask import Flask, make_response, render_template, redirect, request
import flask
import uuid
from flask_bcrypt import generate_password_hash, check_password_hash
from math import ceil
from database_connector import cursor,connection,database_execute_query

from filter_querys.players import build_filter_query_for_players
from filter_querys.teams import build_filter_query_for_teams
from filter_querys.games import build_filter_query_for_games

from utils.team_utils import get_teams_from_page,get_team_name_from_id,team_id_exist,get_team_data_from_id,get_team_members
from utils.cookie_utils import get_cookie_from_user,get_user_from_cookie
from utils.player_utils import get_players_from_page,player_id_exist,get_player_data_from_id
from utils.game_utils import get_games_from_page,game_id_exist,get_game_data_from_id

app = Flask(__name__)

cards_per_page = 100

# Function to set a cookie for a user
def set_cookie(cookie):
    response = make_response(redirect('/'))
    response.set_cookie('session_id', cookie)
    return response

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


@app.route('/', methods=['POST','GET'])
def players():
    session_id = flask.request.cookies.get('session_id')
    if not get_user_from_cookie(session_id):
        return redirect('/login')
    
    if request.method == 'POST':
        player = request.form['playerName']
        position = request.form['playerPosition']
        height = request.form['playerHeight']
        height_sign = request.form['height_sign']
        weight = request.form['playerWeight']
        weight_sign = request.form['weight_sign']
        sort_type = request.form['sortingOption']
        team_name = request.form['teamName']
        sort_order = request.form['sortingOrder']
        page_number = sanitize_current_page(request.form['page'])

        if not player and not position and not height and not weight and not team_name and not sort_type:
            return redirect('/')
        
        parameters_wraped = [player,height,height_sign,weight,weight_sign,position,sort_type,team_name,sort_order]
        query_parameters = build_filter_query_for_players(player,position,height,height_sign,weight,weight_sign,sort_type,team_name,sort_order)
        if query_parameters[0] == "ERROR":
            return redirect('/')
        datas = database_execute_query(query_parameters[0],query_parameters[1])
        # cursor.execute(query_parameters[0],query_parameters[1])
        # datas = cursor.fetchall()
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

@app.route('/teams', methods=['GET','POST'])
def teams():
    session_id = flask.request.cookies.get('session_id')
    if not get_user_from_cookie(session_id):
        return redirect('/login')
    
    if request.method == 'POST':
        height = request.form['playerHeight']
        height_sign = request.form['height_sign']
        weight = request.form['playerWeight']
        weight_sign = request.form['weight_sign']
        sort_type = request.form['sortingOption']
        sort_order = request.form['sortingOrder']
        page_number = sanitize_current_page(request.form['page'])
        if not height and not weight and not sort_type:
            return redirect('/teams',code=302)
        parameters_wraped = [height,height_sign,weight,weight_sign,sort_type,sort_order]
        query_parameters = build_filter_query_for_teams(height,height_sign,weight,weight_sign,sort_type,sort_order)
        if query_parameters[0] == "ERROR":
            return redirect('/')
        datas = database_execute_query(query_parameters[0],query_parameters[1])
        #cursor.execute(query_parameters[0],query_parameters[1])
        #datas = cursor.fetchall()
        total_pages=ceil(len(datas)/cards_per_page)
        datas = datas[(page_number-1)*cards_per_page:page_number*cards_per_page]

        return render_template('teams.html', teams = datas, current_page = page_number, total_pages = total_pages, post = True,parameters = parameters_wraped)
    elif request.method == 'GET':
        current_page = sanitize_current_page(request.args.get("page"))
        total_pages = ceil(get_total_pages("teams")/cards_per_page)
        if current_page > total_pages:
            current_page = total_pages
        
        datas = get_teams_from_page(current_page-1,cards_per_page)
        return render_template('teams.html', teams = datas, current_page = current_page, total_pages = total_pages)

@app.route('/games', methods=['GET','POST'])
def games():
    session_id = flask.request.cookies.get('session_id')
    if not get_user_from_cookie(session_id):
        return redirect('/login')
    
    if request.method == 'POST':
        
        home_team = request.form['homeTeam']
        foreign_team = request.form['foreignTeam']
        home_score = request.form['homeScore']
        home_score_sign = request.form['homeScoreSign']
        foreign_score = request.form['foreignScore']
        foreign_score_sign = request.form['foreignScoreSign']
        date = request.form['date']
        date_sign = request.form['dateSign']
        ecart_score = request.form['ecartScore']
        ecart_sign = request.form['ecartSign']
        # sort_type = request.form['sortingOption']
        sort_order = request.form['sortingOrder']
        winner_team = request.form['winnerTeam']
        page_number = sanitize_current_page(request.form['page'])
        if not home_team and not foreign_team and not home_score and not foreign_score and not date and not ecart_score and not winner_team:
            return redirect('/games')
        print(date)
        parameters_wraped = [home_team,foreign_team,home_score,home_score_sign,foreign_score,foreign_score_sign,date,date_sign,ecart_score,ecart_sign,sort_order,winner_team]
        query_parameters = build_filter_query_for_games(home_team,foreign_team,home_score,home_score_sign,foreign_score,foreign_score_sign,date,date_sign,ecart_score,ecart_sign,sort_order,winner_team)

        if query_parameters[0] == "ERROR":
            return redirect('/')
        datas = database_execute_query(query_parameters[0],query_parameters[1])
        #cursor.execute(query_parameters[0],query_parameters[1])
        #datas = cursor.fetchall()
        total_pages=ceil(len(datas)/cards_per_page)
        datas = datas[(page_number-1)*cards_per_page:page_number*cards_per_page]

        return render_template('games.html', games = datas, current_page = page_number, total_pages = total_pages, post = True,parameters = parameters_wraped)

    elif request.method == 'GET':
        current_page = sanitize_current_page(request.args.get("page"))
        total_pages = ceil(get_total_pages("games")/cards_per_page)
        if current_page > total_pages:
            current_page = total_pages
        
        datas = get_games_from_page(current_page-1,cards_per_page)
        return render_template('games.html', games = datas,current_page = current_page, total_pages = total_pages)

@app.route('/player', methods = ['GET'])
def player():
    session_id = flask.request.cookies.get('session_id')
    if not get_user_from_cookie(session_id):
        return redirect('/login')
    player_id = request.args.get("player_id")
    data = []
    if player_id_exist(player_id):
        data = get_player_data_from_id(player_id)
    else:
        return redirect('/')
    if team_id_exist(data[6]):
        team_name = get_team_name_from_id(data[6])
    else:
        return redirect('/')
    return render_template('player.html',player = data,team_name=team_name)

@app.route('/team', methods = ['GET','POST'])
def team():
    session_id = flask.request.cookies.get('session_id')
    if not get_user_from_cookie(session_id):
        return redirect('/login')
    
    if request.method == 'GET':
        team_id = request.args.get("team_id")
        data = []
        if team_id_exist(team_id):
            data = get_team_data_from_id(team_id)
            print(data)
        else:
            return redirect('/team')
        team_players = get_team_members(team_id)
        return render_template('team.html',team=data,players=team_players)
    elif request.method == 'POST':
        player = request.form['playerName']
        position = request.form['playerPosition']
        height = request.form['playerHeight']
        height_sign = request.form['height_sign']
        weight = request.form['playerWeight']
        weight_sign = request.form['weight_sign']
        sort_type = request.form['sortingOption']
        team_name = get_team_name_from_id(request.form['teamId'])
        sort_order = request.form['sortingOrder']
        if not player and not position and not height and not weight and sort_type == "alphabetical":
            return redirect('/team?team_id='+ request.form['teamId'])
        data = []
        if team_id_exist(request.form['teamId']):
            data = get_team_data_from_id(request.form['teamId'])
        else:
            return redirect('/teams')
        parameters_wraped = [player,height,height_sign,weight,weight_sign,position,sort_type,team_name,sort_order]
        query_parameters = build_filter_query_for_players(player,position,height,height_sign,weight,weight_sign,sort_type,team_name,sort_order)
        if query_parameters[0] == "ERROR":
            return redirect('/team?team_id='+ request.form['teamName'])
        team_players = database_execute_query(query_parameters[0],query_parameters[1])
        print(parameters_wraped)
        return render_template('team.html',team=data,players=team_players,parameters = parameters_wraped,post = True)

@app.route('/game', methods = ['GET'])
def game():
    session_id = flask.request.cookies.get('session_id')
    if not get_user_from_cookie(session_id):
        return redirect('/login')
    
    game_id = request.args.get("game_id")
    data = []
    if game_id_exist(game_id):
        data = get_game_data_from_id(game_id)
    else:
        return redirect('/games')
    
    home_team_data = get_team_data_from_id(data[1])
    visitor_team_data = get_team_data_from_id(data[8])
    return render_template('game.html',game=data,home_team = home_team_data,visitor_team = visitor_team_data)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    session_id = flask.request.cookies.get('session_id')
    if get_user_from_cookie(session_id):
        return redirect('/')
    if flask.request.method == 'GET':
        session_id = flask.request.cookies.get('session_id')
        user = get_user_from_cookie(session_id)
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    session_id = flask.request.cookies.get('session_id')
    if get_user_from_cookie(session_id):
        return redirect('/')
    if flask.request.method == 'GET':
        session_id = flask.request.cookies.get('session_id')
        user = get_user_from_cookie(session_id)
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