from . import strings_to_sign

def build_filter_query_for_games(home_team,foreign_team,home_score,home_score_sign,foreign_score,foreign_score_sign,date,date_sign,ecart_score,ecart_sign,sort_order,winner_team,game_state):
    query = 'SELECT game_id,attack.abbreviation,defense.abbreviation,game_date FROM games JOIN teams as attack ON visitor_team_id = attack.team_id JOIN teams as defense ON home_team_id = defense.team_id'
    original_query = query + " WHERE"
    parameters = []
    arbitre=True

    if home_team:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        # home_id = get_team_id_from_name(home_team)[0]
        query = query + " (defense.team_name = %s OR defense.abbreviation = %s)"
        parameters.append(home_team)
        parameters.append(home_team)

    if foreign_team:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        # visitor_id = get_team_id_from_name(foreign_team)[0]
        if query == original_query:
            query = query + " (attack.team_name = %s OR attack.abbreviation = %s)"
        else:
            query = query + " AND (attack.team_name = %s OR attack.abbreviation = %s)"
        parameters.append(foreign_team)
        parameters.append(foreign_team)
    
    if winner_team:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        # visitor_id = get_team_id_from_name(foreign_team)[0]
        if query == original_query:
            query = query + " ( ((attack.team_name = %s OR attack.abbreviation = %s) AND visitor_team_score > home_team_score) OR ((defense.team_name = %s OR defense.abbreviation = %s) AND home_team_score > visitor_team_score) )"
        else:
            query = query + " AND ( ((attack.team_name = %s OR attack.abbreviation = %s) AND visitor_team_score > home_team_score) OR ((defense.team_name = %s OR defense.abbreviation = %s) AND home_team_score > visitor_team_score) )"
        parameters.append(winner_team)
        parameters.append(winner_team)
        parameters.append(winner_team)
        parameters.append(winner_team)

    if home_score:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if home_score_sign in strings_to_sign:
            if query == original_query:
                query = query + " home_team_score " + strings_to_sign[home_score_sign] +" %s"
            else:
                query = query + " AND home_team_score " + strings_to_sign[home_score_sign] +" %s"
            parameters.append(home_score)
        else:
            return "ERROR",[]
        
    if foreign_score:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if foreign_score_sign in strings_to_sign:
            if query == original_query:
                query = query + " visitor_team_score " + strings_to_sign[foreign_score_sign] +" %s"
            else:
                query = query + " AND visitor_team_score " + strings_to_sign[foreign_score_sign] +" %s"
            parameters.append(foreign_score)
        else:
            return "ERROR",[]
    if game_state:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if query == original_query:
            if game_state == "final":
                query = query + " game_status = %s"
                parameters.append(game_state)
            elif game_state == "during":
                query = query + " LENGTH(game_status) < 10 AND game_status != 'final'"
            elif game_state == "coming":
                query = query + " periode = 0"
            else:
                return "ERROR",[]
        else:
            if game_state == "final":
                query = query + " AND game_status = %s"
                parameters.append(game_state)
            elif game_state == "during":
                query = query + " AND periode != 0 AND game_status != 'final'"
            elif game_state == "coming":
                query = query + " AND periode = 0"
            else:
                return "ERROR",[]
    if date:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if date_sign in strings_to_sign:
            if date_sign == "eq":
                sign = "LIKE"
                parameters.append("%" + date + "%")
            else:
                sign = strings_to_sign[date_sign]
                parameters.append(date)
            if query == original_query:
                query = query + " game_date " + sign + " %s"
            else:
                query = query + " AND game_date " + sign + " %s"
        else:
            return "ERROR",[]
    
    if ecart_score:
        if arbitre:
            query = query + " WHERE"
            arbitre = False
        if ecart_sign in strings_to_sign:
            if query == original_query:
                query = query + " ABS(home_team_score - visitor_team_score) " + strings_to_sign[ecart_sign] + " %s"
            else:
                query = query + " AND ABS(home_team_score - visitor_team_score) " + strings_to_sign[ecart_sign] + " %s"
            parameters.append(ecart_score)
        else:
            return "ERROR",[]
    
    if sort_order != "DESC" and sort_order != "ASC":
        return "ERROR",[]
    else:
        query = query + " ORDER BY game_date " + sort_order
    print(query)
    return [query,parameters]