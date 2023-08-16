from . import strings_to_sign

def build_filter_query_for_teams(height,height_sign,weight,weight_sign,sort_type,sort_order):
    query="SELECT players.team_id,teams.team_name FROM players JOIN teams ON teams.team_id = players.team_id GROUP BY players.team_id,teams.team_name"
    original_query = query + " HAVING"
    parameters = []
    arbitre=True
    if height:
        if arbitre:
            query = query + " HAVING"
            arbitre = False
        if height_sign in strings_to_sign:
            if query == original_query:
                query = query + " AVG((height_feet * 0.3048) + (height_inches * 0.0254)) " + strings_to_sign[height_sign] + " %s"
            parameters.append(height)
        else:
            return "ERROR"
    if weight:
        if arbitre:
            query = query + " HAVING"
            arbitre = False
        if weight_sign in strings_to_sign:
            if query == original_query:
                query = query + " AVG(weight_pounds) " + strings_to_sign[weight_sign] + " %s"
            else:
                query = query + " AND AVG(weight_pounds) " + strings_to_sign[weight_sign] + " %s"
            parameters.append(round(float(weight) * 2.20462))
        else:
            return "ERROR",[]
    if sort_type:
        if sort_order != "DESC" and sort_order != "ASC":
            return "ERROR",[]
        if sort_type == "alphabetical":
            query = query + " ORDER BY teams.team_name "+ sort_order
        elif sort_type == "height":
            if height:
                query = query[:38] + ",AVG((height_feet * 0.3048) + (height_inches * 0.0254)) as taille_moy" + query[38:] + " ORDER BY taille_moy " + sort_order
            else:
                query = query[:38] + ",AVG((height_feet * 0.3048) + (height_inches * 0.0254)) as taille_moy" + query[38:] + " ORDER BY taille_moy " + sort_order
        elif sort_type == "weight":
            if weight:
                query = query[:38] + ",AVG(weight_pounds) as poids_moy" + query[38:] + " ORDER BY poids_moy " + sort_order
            else:
                query = query[:38] + ",AVG(weight_pounds) as poids_moy" + query[38:] + " ORDER BY poids_moy " + sort_order
    return [query,parameters]