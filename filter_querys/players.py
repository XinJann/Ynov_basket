from database_connector import database_execute_query
from . import strings_to_sign
from utils.team_utils import get_team_id_from_name

def build_filter_query_for_players(player : str,position,height,height_sign,weight,weight_sign,sort_type,team_name,sort_order):
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
                query = query + " (height_feet * 0.3048) + (height_inches * 0.0254) " + strings_to_sign[height_sign] + " %s"
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
            return "ERROR",[]
    if position:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if query == original_query:
            query = query + " position LIKE %s"
        else:
            query = query + " AND position LIKE %s"
        parameters.append("%" + position + "%")
    if team_name:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        
        team_id = get_team_id_from_name(team_name)
        parameters.append(team_id)
        # Faire une fonction qui récupe le team_id en fonction du nom
        #team_id = database_execute_query('SELECT team_id FROM teams WHERE team_name  = %s',(team_name,),"one")
        #if team_id:
        #    parameters.append(team_id[0])
        #else:
        #    parameters.append(team_id)
        # cursor.execute('SELECT team_id FROM teams WHERE team_name  = %s',(team_name,))
        # team_id = cursor.fetchone()[0]

        if query == original_query:
            query = query + " team_id = %s"
        else:
            query = query + " AND team_id = %s"
    if sort_type:
        if sort_order != "DESC" and sort_order != "ASC":
            return "ERROR",[]
        if sort_type == "alphabetical":
            query = query + " ORDER BY first_name "+ sort_order +",last_name " + sort_order
        elif sort_type == "height":
            query = query + " ORDER BY height_feet " + sort_order + ",height_inches " + sort_order
        elif sort_type == "weight":
            query = query + " ORDER BY weight_pounds " + sort_order
    return [query,parameters]