from fastapi import FastAPI
import uvicorn
import database
import sys
import os
import subprocess


def StartUp():
    connection = database.connect()
    database.create_tables(connection)
    return connection


app = FastAPI()
StartUp()

@app.get("/GetAllUsers")
def getallusers():
    connection = StartUp()
    result = database.get_all_users(connection)
    return {"result": result}


@app.get("/UpdateApp")
def update():
    sp = subprocess.Popen("git pull", shell=True, stdout=subprocess.PIPE)
    subprocess_return = sp.stdout.read()
    subprocess_return = subprocess_return.decode('utf-8')
    return subprocess_return


@app.get("/DashboardSignIn")
def dashboardsignin(username: str, password: str):
    connection = StartUp()
    result = database.dashboard_signin(connection, username, password)
    return {"result": result}


@app.get("/RegisterUser")
def registeruser(company: str, uuid: str, password: str, macid: str):
    connection = StartUp()
    result = database.register_user(
        connection, company, uuid, password, macid)
    return {"result": result}


@app.get("/")
@app.get("/Test")
def test():
    return {"welcome": "working"}


if "__main__" == __name__:
    uvicorn.run("app:app", host='0.0.0.0', port=8000,
                reload=True, debug=True, workers=3)
