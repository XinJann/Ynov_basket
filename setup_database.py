import mysql.connector
import requests
import json
import time

API_url_players = "https://www.balldontlie.io/api/v1/players?per_page=100"
API_url_teams = "https://www.balldontlie.io/api/v1/teams?per_page=100"
API_url_games = "https://www.balldontlie.io/api/v1/games?per_page=100"

with open('credentials.txt','r') as f:
    lines = f.readlines()
    database = lines[0].replace('\n','')
    user = lines[1].replace('\n','')
    password = lines[2].replace('\n','')
    host = lines[3].replace('\n','')

connection = mysql.connector.connect(host=host,
                                         database=database,
                                         user=user,
                                         password=password)

cursor = connection.cursor()

def executeScriptsFromFile(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        if command.strip() != '':
            cursor.execute(command)

executeScriptsFromFile('script.sql')

def add_player_to_database(player):
    cursor.execute('INSERT INTO players (player_id, first_name, height_feet, height_inches, last_name, position, team_id, weight_pounds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (player["id"], player["first_name"], player["height_feet"], player["height_inches"], player["last_name"], player["position"], player["team"]["id"], player["weight_pounds"]))
    connection.commit()

def player_exist_in_database(player):
    cursor.execute('SELECT player_id FROM players WHERE player_id=%s', (player["id"],))
    existing_user = cursor.fetchone()
    if existing_user:
        return True
    else:
        return False

def add_team_to_database(team):
    cursor.execute('INSERT INTO teams (team_id, abbreviation, city, conference, division, full_name, team_name) VALUES (%s, %s, %s, %s, %s, %s, %s)', (team["id"], team["abbreviation"], team["city"], team["conference"], team["division"], team["full_name"], team["name"]))
    connection.commit()

def team_exist_in_database(team):
    cursor.execute('SELECT team_id FROM teams WHERE team_id=%s', (team["id"],))
    existing_user = cursor.fetchone()
    if existing_user:
        return True
    else:
        return False

def add_game_to_database(game):
    cursor.execute('INSERT INTO games (game_id, game_date, home_team_id, home_team_score, periode, postseason, season, game_status, game_time, visitor_team_id, visitor_team_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (game["id"], game["date"], game["home_team"]["id"], game["home_team_score"], game["period"], game["postseason"], game["season"], game["status"], game["time"], game["visitor_team"]["id"], game["visitor_team_score"]))
    connection.commit()

def game_exist_in_database(game):
    cursor.execute('SELECT game_id FROM games WHERE game_id=%s', (game["id"],))
    existing_user = cursor.fetchone()
    if existing_user:
        return True
    else:
        return False

def get_players_data_from_API(url):
    print("##### Starting extracting players datas #####")
    finish = False
    actual_page=1
    while not finish:
        time.sleep(0.5)
        if actual_page % 100 == 0:
            # Sleep de 5 sec pck sinon on se fait block
            time.sleep(4)
        request = requests.get(url + "&page=" + str(actual_page))
        data = json.loads(request.text)
        for player in data["data"]:
            if not player_exist_in_database(player):
                add_player_to_database(player)
                print(player["first_name"] + " " + player["last_name"] + " added in database")
        actual_page = data["meta"]["next_page"]
        if actual_page == None:
            finish = True
    print("##### Players extracted #####")

def get_teams_data_from_API(url):
    print("##### Starting extracting teams datas #####")
    finish = False
    actual_page=1
    while not finish:
        request = requests.get(url + "&page=" + str(actual_page))
        data = json.loads(request.text)
        for team in data["data"]:
            if not team_exist_in_database(team):
                add_team_to_database(team)
                print(team["full_name"] + " " + " added in database")
        actual_page = data["meta"]["next_page"]
        if actual_page == None:
            finish = True
    print("##### Teams extracted #####")

def get_games_data_from_API(url):
    print("##### Starting extracting games datas #####")
    finish = False
    actual_page=1
    total_added = 0
    while not finish:
        time.sleep(0.5)
        if actual_page % 100 == 0:
            # Sleep de 5 sec pck sinon on se fait block
            print("Sleeping for 5 sec")
            time.sleep(5)
            print("Resume")
        request = requests.get(url + "&page=" + str(actual_page))
        if (len(request.text) < 150): # Cas ou l'API nous block
            print(request.text)
        data = json.loads(request.text)
        for game in data["data"]:
            if not game_exist_in_database(game):
                add_game_to_database(game)
                total_added += 1
        actual_page = data["meta"]["next_page"]
        if actual_page == None:
            finish = True
    print( str(total_added) + " new games added in database")
    print("##### Games extracted #####")

def get_data_from_API():
    print("####### Starting refreshing datas #######")
    get_players_data_from_API(API_url_players)
    get_teams_data_from_API(API_url_teams)
    get_games_data_from_API(API_url_games)