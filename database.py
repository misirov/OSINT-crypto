import ast
import sqlite3
import pathlib
from sqlite3 import Error


db = "koiosint.db"

def create_connection():
    db_file = r"" + db
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table():
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                            user text UNIQUE PRIMARY KEY,
                                            friends text NOT NULL
                                        ); """

    conn = create_connection()

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_users_table)
        except Error as e:
            print(e)
    else:
        print("Error! Cannot create the db connection")


def add_user(user):
    conn = create_connection()
    with conn:
        sql = ''' INSERT or IGNORE INTO users(user, friends)
                      VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (user, ""))
        conn.commit()


def update_friends(user, friends):
    conn = create_connection()

    if len(query_user(user)) <= 0:
        add_user(user)

    with conn:
        sql = ''' UPDATE users SET friends = ? WHERE user = ?'''
        cur = conn.cursor()
        cur.execute(sql, (friends, user))
        conn.commit()


def query_user(user):
    conn = create_connection()

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user=?", (user,))

        rows = cur.fetchall()
        return rows


def query_friends(user):
    conn = create_connection()

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT friends FROM users WHERE user=?", (user,))

        rows = cur.fetchall()
        return ast.literal_eval(rows[0][0])

