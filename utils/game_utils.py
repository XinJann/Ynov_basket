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