import sqlite3


connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users(id int, username text, password text, mail text, carplate text, phone text) "
cursor.execute(create_table)


create_table = "CREATE TABLE IF NOT EXISTS slotes(slote1 int,slote2 int,slote3 int,slote4 int)"
cursor.execute(create_table)


connection.commit()
connection.close()
