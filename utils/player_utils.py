from database_connector import database_execute_query

def get_players_from_page(page_number,cards_per_page):
    #cursor.execute('SELECT player_id,first_name, last_name FROM players LIMIT %s OFFSET %s', (cards_per_page,page_number*cards_per_page))
    return database_execute_query('SELECT player_id,first_name, last_name FROM players LIMIT %s OFFSET %s', (cards_per_page,page_number*cards_per_page))
    #return cursor.fetchall()

def player_id_exist(player_id):
    player = database_execute_query('SELECT * FROM players WHERE player_id = %s',(player_id,))
    if len(player) == 1:
        return True
    else:
        return False

def get_player_data_from_id(player_id):
    return database_execute_query('SELECT first_name,last_name,position,height_feet,height_inches,weight_pounds,team_id FROM players WHERE player_id = %s',(player_id,),"one")