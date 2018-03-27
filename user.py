import sqlite3

class userModel():
    def __init__(self, id, username, password, mail, carplate, phone):                               #there is a(_)before id because it already a basic element in a python.
        self.id = id
        self.username = username
        self.password = password
        self.mail = mail
        self.carplate = carplate
        self.phone = phone

    @classmethod                                                            #that is mean we use the current class so er replaces (self) with cls.
    def find_by_username(cls,username):
        connection =sqlite3.connect('data.db')
        cursor = connection.cursor()
        query  = "SELECT * FROM users WHERE username=?"                     #select the row which contain this (username).
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4], row[5])
        else:
            user= None

        connection.close()

        return user




    @classmethod                                                             # that is mean we use the current class so er replaces (self) with cls.
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query,(id,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4], row[5])
        else:
            user = None

        connection.close()

        return user

