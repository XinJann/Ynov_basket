from database_connector import database_execute_query

def get_games_from_page(page_number,cards_per_page):
    #cursor.execute("""
#SELECT game_id,attack.abbreviation,defense.abbreviation,game_date FROM games 
#JOIN teams as attack ON home_team_id = attack.team_id
#JOIN teams as defense ON visitor_team_id = defense.team_id
#LIMIT %s OFFSET %s;
#""", (cards_per_page,page_number*cards_per_page))
    return database_execute_query("""
SELECT game_id,attack.abbreviation,defense.abbreviation,game_date FROM games 
JOIN teams as attack ON home_team_id = attack.team_id
JOIN teams as defense ON visitor_team_id = defense.team_id
LIMIT %s OFFSET %s;
""", (cards_per_page,page_number*cards_per_page))
    #return cursor.fetchall()

def game_id_exist(game_id):
    game = database_execute_query('SELECT * FROM games WHERE game_id = %s',(game_id,))
    if len(game) == 1:
        return True
    else:
        return False

def get_game_data_from_id(game_id):
    return database_execute_query('SELECT game_date,home_team_id,home_team_score,periode,postseason,season,game_status,game_time,visitor_team_id,visitor_team_score FROM games WHERE game_id = %s',(game_id,),"one")
