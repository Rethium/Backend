import sqlite3
import json

# table creation statements
CREATE_USER_TABLE = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, uuid TEXT, password TEXT, company TEXT, macid TEXT);'
CREATE_DASHBOARD_ADMIN = 'CREATE TABLE IF NOT EXISTS admins (id INTEGER PRIMARY KEY, name TEXT, password TEXT);'
CREATE_DATA_TABLE = 'CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, uuid TEXT, timestamp TEXT, data TEXT);'
# new queries
GET_ALL_USERS = 'SELECT * FROM users'
CHECK_IF_USER_EXISTS = 'SELECT * FROM users WHERE uuid = ? AND password = ? AND company = ?'
CHECK_IF_USER_DELETED = 'SELECT * FROM users WHERE uuid = ? AND company = ?'
CHECK_IF_ADMIN_EXISTS = 'SELECT * FROM admins WHERE name = ? AND password = ?;'
ADD_ADMIN = 'INSERT INTO admins (name, password) VALUES (?, ?);'
REGISTER_USER = 'INSERT INTO users (company, uuid, password, macid) VALUES (?, ?, ?, ?);'
DELETE_USER = 'DELETE FROM users WHERE uuid = ? AND company = ?'
GET_MAC_ID_OF_USER = 'SELECT macid FROM users WHERE uuid = ? AND password = ? AND company = ?'
EDIT_MAC_ID = 'UPDATE users SET macid = ? WHERE uuid = ? AND password = ? AND company = ?'
GET_COLUMN_NAMES_FOR_USER_TABLE = 'PRAGMA table_info(users);'
PUSH_DATA = 'INSERT INTO data (uuid, timestamp, data) VALUES (?, ?, ?);'
GET_DATA = 'SELECT * FROM data WHERE uuid = ? AND timestamp = ? ;'
GET_ALL_DATA = 'SELECT * FROM data WHERE uuid = ?;'
DELETE_ALL_USERS = 'DELETE FROM users;'


# new queries


def connect():
    return sqlite3.connect('database.db')


def create_tables(connection):
    with connection:
        connection.execute(CREATE_USER_TABLE)
        connection.execute(CREATE_DASHBOARD_ADMIN)
        connection.execute(CREATE_DATA_TABLE)


def get_all_users(connection):
    with connection:
        result = connection.execute(GET_ALL_USERS).fetchall()
        return result


def check_if_user_exists(connection, uuid, password, company):
    with connection:
        val = connection.execute(CHECK_IF_USER_EXISTS,
                                 (uuid, password, company)).fetchone()
        if val is None:
            return{"status": "failure", "message": "incorrect combination of username, password and company"}
        return {"status": "success", "macid": val[-1]}


def register_user(connection, uuid, password, company, macid):
    check_user = check_if_user_exists(connection, uuid, password, company)
    if(check_user["status"] == "success"):
        return {"status": "failure", "message": "user already exists"}
    else:
        with connection:
            connection.execute(REGISTER_USER, (company, uuid, password, macid))
            return check_if_user_exists(connection, uuid, password, company)


def delete_user(connection, uuid, company):
    with connection:
        connection.execute(DELETE_ALL_USERS)
        result = connection.execute(
            CHECK_IF_USER_DELETED, (uuid, company)).fetchone()
        if result is None:
            return {"status": "success", "message": "user deleted successfully"}
        else:
            return {"status": "failure", "message": "user not deleted"}


def view_all_users(connection):
    with connection:
        result = connection.execute(GET_ALL_USERS).fetchall()
        print(result)
        return result


def dashboard_signin(connection, username, password):
    with connection:
        result = connection.execute(
            CHECK_IF_ADMIN_EXISTS, (username, password)).fetchone()
        if result is None:
            return {"status": "failure", "message": "incorrect username or password"}
        else:
            return {"status": "success", "message": "admin logged in successfully"}


def dashboard_signup(connection, username, password, secretkey):
    config = None
    with open("config.json", "r+") as f:
        config = f.read()
    config = json.loads(config)
    Json_secretkey = config["secretkey"]
    if(Json_secretkey == secretkey):
        with connection:
            connection.execute(ADD_ADMIN, (username, password)).fetchone()
            return {"status": "success", "message": "admin added successfully"}
    else:
        {"status": "failure", "message": "secretkey is incorrect"}


def get_column_names(connection):
    with connection:
        column_info = connection.execute(
            GET_COLUMN_NAMES_FOR_USER_TABLE).fetchall()
        columns = [entity[1] for entity in column_info]
        return columns


def push_data(connection, uuid, timestamp, data):
    with connection:
        connection.execute(PUSH_DATA, (uuid, timestamp, data))
        return {"status": "success"}


def get_data(connection, uuid, timestamp):
    if(timestamp == ""):
        return get_all_data(connection, uuid)
    with connection:
        return connection.execute(GET_DATA, (uuid, timestamp)).fetchone()


def get_all_data(connection, uuid):
    with connection:
        val = connection.execute(GET_ALL_DATA, (uuid,)).fetchall()
        return val
