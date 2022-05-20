from fastapi import FastAPI
import uvicorn
import database
import subprocess


def StartUp():
    connection = database.connect()
    database.create_tables(connection)
    return connection


app = FastAPI()


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
    return result


@app.get("/DashboardSignUp")
def dashboardsignup(username: str, password: str, secretkey: str):
    connection = StartUp()
    result = database.dashboard_signup(connection, username, password,secretkey)
    return {"result": result}


@app.get("/RegisterUser")
def registeruser(company: str, uuid: str, password: str, macid: str):
    connection = StartUp()
    result = database.register_user(
        connection, company, uuid, password, macid)
    return {"result": result}


@app.get("/UserSignin")
def userSignin(uuid: str, password: str, company: str):
    connection = StartUp()
    result = database.check_if_user_exists(
        connection, uuid, password, company)
    return {"result": result}


@app.get("/PushData")
def pushData(uuid: str, timestamp: str, data: str):
    connection = StartUp()
    result = database.push_data(connection, uuid, timestamp, data)
    return {"result": result}


@app.get("/GetData")
def getData(uuid: str, timestamp: str = ""):
    connection = StartUp()
    result = database.get_data(connection, uuid, timestamp)
    return result


@app.get("/")
def home():
    connection = StartUp()
    return {"result": "Hello World"}


if "__main__" == __name__:
    uvicorn.run("app:app", host='0.0.0.0', port=8000,
                reload=True, debug=True, workers=3)
