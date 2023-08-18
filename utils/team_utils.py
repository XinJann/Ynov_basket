from database_connector import database_execute_query

def get_teams_from_page(page_number,cards_per_page):
    # cursor.execute('SELECT team_id,team_name FROM teams LIMIT %s OFFSET %s', (cards_per_page,page_number*cards_per_page))
    return database_execute_query('SELECT team_id,team_name FROM teams LIMIT %s OFFSET %s', (cards_per_page,page_number*cards_per_page))
    # return cursor.fetchall()

def get_team_id_from_name(name):
    # cursor.execute('SELECT team_id FROM teams WHERE team_name = %s',(name,))
    # return cursor.fetchone()
    team_id = database_execute_query('SELECT team_id FROM teams WHERE team_name = %s',(name,),"one")
    if team_id:
        return team_id[0]
    else:
        return team_id

def team_id_exist(team_id):
    team = database_execute_query('SELECT * FROM teams WHERE team_id = %s',(team_id,))
    if len(team) == 1:
        return True
    else:
        return False

# les fonctions qui suivent sont à utiliser après verif de "team_id_exist"
def get_team_name_from_id(team_id):
    return database_execute_query('SELECT team_name FROM teams WHERE team_id = %s',(team_id,),"one")[0]

def get_team_data_from_id(team_id):
    return database_execute_query('SELECT team_id,abbreviation,city,conference,division,full_name,team_name FROM teams WHERE team_id = %s',(team_id,),"one")

def get_team_members(team_id):
    return database_execute_query('SELECT player_id,first_name,last_name FROM players WHERE team_id = %s ORDER BY first_name,last_name',(team_id,))