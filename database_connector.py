import mysql.connector

database =""
user=""
password=""
host=""

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

def database_execute_query(query,parameters,render="all"):
    cursor.execute(query,parameters)
    if render == "all":
        return cursor.fetchall()
    elif render == "one":
        return cursor.fetchone()