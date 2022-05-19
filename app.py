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


@app.get("/BMSUserSignIn")
def read_item_signin(username: str, password: str):
    connection = StartUp()
    result = database.validate_user(connection, username, password)
    return {"result": result}


@app.get("/BMSUserSignUp")
def read_item_signup(username: str, password: str, company: str):
    connection = StartUp()
    print(database.add_user(connection, username, password, company))
    return {"username": username, "password": password, "company": company, "status": "success"}


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

@app.get("/")
@app.get("/Test")
def test():
    return {"welcome": "working"}

if "__main__" == __name__:
    uvicorn.run("app:app",host='0.0.0.0', port=8000, reload=True, debug=True, workers=3)