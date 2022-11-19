from datetime import datetime, timedelta
import sqlite3
import json
import os
from constants.SQLite_commands import *
from constants.envs import *


def connect():

    return sqlite3.connect('database/database.db')


def create_tables(connection):
    tables = [CREATE_COMPANY_TABLE, CREATE_USER_TABLE,
              CREATE_DATA_TABLE, CREATE_DASHBOARD_ADMIN]
    with connection:
        for table in tables:
            connection.execute(table)


def get_all_users(connection, JSON=False):
    with connection:
        result = connection.execute(GET_ALL_USERS).fetchall()
        if JSON:
            result_dict = {}
            for x in range(len(result)):
                temp = {result[x][0]: {
                    "uuid": result[x][3],
                    "password": result[x][1],
                    "company": result[x][2],
                    "macid": result[x][4]
                }}
                result_dict.update(temp)
                return result_dict
        return result


def check_if_user_exists(connection, uuid, password, company):
    with connection:
        val = connection.execute(CHECK_IF_USER_EXISTS,
                                 (uuid, password, company)).fetchone()
        if val is None:
            return {"status": "failure", "message": "incorrect combination of uuid, password and company"}
        return {"status": "success", "macid": val[-1]}


def register_user(connection, uuid, password, company, macid):
    check_user = check_if_user_exists(connection, uuid, password, company)
    if (check_user["status"] == "success"):
        return {"status": "failure", "message": "user already exists"}
    else:
        with connection:
            connection.execute(REGISTER_USER, (uuid, password, company, macid))
            return check_if_user_exists(connection, uuid, password, company)


def check_if_company_exists(connection, company):
    with connection:
        val = connection.execute(CHECK_COMPANY_EXISTS, (company,)).fetchone()
        if val is None:
            return {"status": "failure", "message": "company does not exist"}
        return {"status": "success", "message": "company exists"}


def register_company(connection, company):
    check_company = check_if_company_exists(connection, company)
    if (check_company["status"] == "success"):
        return {"status": "failure", "message": "company already exists"}
    else:
        with connection:
            connection.execute(REGISTER_COMPANY, (company,))
            return check_if_company_exists(connection, company)


def get_all_companies(connection):
    with connection:
        result = connection.execute(GET_ALL_COMPANIES).fetchall()
        listofcompanies = list()
        for x in result:
            listofcompanies.append(x[0])
        return listofcompanies


def delete_user(connection, uuid, company):
    with connection:
        connection.execute(DELETE_USER, (uuid, company))
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
    if (SECRET_KEY == secretkey):
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


def push_data(connection, uuid, timestamp, data, macid):
    now = datetime.utcnow()
    now = now+timedelta(hours=5, minutes=30)
    current_time = now.strftime("%H:%M:%S")
    today = now.strftime("%d-%m-%Y")
    update_time = current_time+" "+today
    timestamp = update_time
    with connection:
        connection.execute(PUSH_DATA, (uuid, timestamp, data, macid))
        return {"status": "success"}


def get_data(connection, uuid, timestamp, macid):
    if (timestamp == ""):
        return get_all_data(connection, uuid)
    with connection:
        vals = connection.execute(
            GET_DATA, (uuid, timestamp, macid)).fetchone()
        if vals is None:
            return {}
        else:
            print(vals)
            return {"id": vals[0], "uuid": vals[1], "timestamp": vals[2], "data": vals[3], "macid": vals[4]}


def get_all_data(connection, uuid):
    with connection:
        val = connection.execute(GET_ALL_DATA, (uuid,)).fetchall()
        returnvals = {}
        print(*val, sep="\n")
        for x in range(len(val)):
            returnvals[x] = {
                "id": val[x][0],
                "uuid": val[x][1],
                "timestamp": val[x][2],
                "data": val[x][3],
                "macid": val[x][4]
            }
        return returnvals


def get_all_data_2(connection):
    val = connection.execute(GET_ALL_DATA_2).fetchall()
    returnvals = {}
    max_serve = 1000
    start = 0 if len(val) < max_serve else len(val)-max_serve
    for x in range(start, len(val)):
        returnvals[x] = {
            "id": val[x][0],
            "uuid": val[x][1],
            "timestamp": val[x][2],
            "data": val[x][3],
            "macid": val[x][4]
        }
    return returnvals


def download_data(connection):
    val = connection.execute(GET_ALL_DATA_2).fetchall()
    returnvals = {}
    for x in range(len(val)):
        returnvals[x] = {
            "id": val[x][0],
            "uuid": val[x][1],
            "timestamp": val[x][2],
            "data": val[x][3],
            "macid": val[x][4]
        }
    file = os.path.join(os.getcwd(), "public", "downloads", "data.json")
    with (open(file, "w")) as f:
        json.dump(returnvals, f)
    return file


def excete_on_sqlite(connection, command, secretkey):
    if (SECRET_KEY == secretkey):
        with connection:
            connection.execute(command)
            return {"status": "success", "message": "command executed successfully"}
