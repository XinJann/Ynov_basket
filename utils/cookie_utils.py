from database_connector import database_execute_query

def get_cookie_from_user(user_id):
    #cursor.execute('SELECT cookie FROM users WHERE id=%s', (user_id,))
    #result = cursor.fetchone()
    result = database_execute_query('SELECT cookie FROM users WHERE id=%s', (user_id,),"one")
    if result:
        return result[0]
    else:
        return result

def get_user_from_cookie(cookie):
    #cursor.execute('SELECT username FROM users WHERE cookie=%s', (cookie,))
    #result = cursor.fetchone()
    result = database_execute_query('SELECT username FROM users WHERE cookie=%s', (cookie,),"one")
    if result:
        return result[0]
    else:
        return result