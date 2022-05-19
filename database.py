import sqlite3

# table creation statements
CREATE_USER_TABLE = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, uuid TEXT, password TEXT, company TEXT, macid TEXT);'
CREATE_DASHBOARD_ADMIN = 'CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, name TEXT, password TEXT);'

# new queries
GET_ALL_USERS = 'SELECT * FROM users;'
CHECK_IF_USER_EXISTS = 'SELECT * FROM users WHERE uuid = ? AND password = ? AND company = ?'
CHECK_IF_ADMIN_EXISTS = 'SELECT * FROM admins WHERE name = ? AND password = ?;'
REGISTER_USER = 'INSERT INTO users (company, uuid, password, macid) VALUES (?, ?, ?, ?);'
GET_MAC_ID_OF_USER = 'SELECT macid FROM users WHERE uuid = ? AND password = ? AND company = ?'
EDIT_MAC_ID = 'UPDATE users SET macid = ? WHERE uuid = ? AND password = ? AND company = ?'
GET_COLUMN_NAMES_FOR_USER_TABLE = 'PRAGMA table_info(users);'


# new queries


def connect():
    return sqlite3.connect('data.db')


def create_tables(connection):
    with connection:
        connection.execute(CREATE_USER_TABLE)
        connection.execute(CREATE_DASHBOARD_ADMIN)


def get_all_users(connection):
    with connection:
        return connection.execute(GET_ALL_USERS).fetchall()


def check_if_user_exists(connection, username, password, company):
    with connection:
        return connection.execute(CHECK_IF_USER_EXISTS,
                                  (username, password, company)).fetchone()


def dashboard_signin(connection, username, password):
    with connection:
        return connection.execute(CHECK_IF_ADMIN_EXISTS, (username, password)).fetchone()


def register_user(connection, name, password, company):
    with connection:
        pass


def get_column_names(connection):
    with connection:
        column_info = connection.execute(
            GET_COLUMN_NAMES_FOR_USER_TABLE).fetchall()
        columns = [entity[1] for entity in column_info]
        return columns
