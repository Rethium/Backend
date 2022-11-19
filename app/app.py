from fastapi import FastAPI
import uvicorn
import database
import subprocess
import logging
import setup_instance
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os


def StartUp():
    connection = database.connect()
    database.create_tables(connection)
    return connection


def run_subprocess(command):
    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    subprocess_return = sp.stdout.read()
    subprocess_return = subprocess_return.decode('utf-8')
    return subprocess_return


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5050",
    "http://143.110.176.59",
    "https://143.110.176.59",
    "http://143.110.176.59:5050/",
    "https://143.110.176.59:5050/",
    "*"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="public"), name="public")

logging.basicConfig(
    filename='logs/app.log',
    filemode='a',
    level=logging.DEBUG,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


@app.get("/GetAllUsers")
def getallusers():
    connection = StartUp()
    query_result = database.get_all_users(connection)
    result = {}
    for x in range(len(query_result)):
        temp = {query_result[x][0]: {
            "uuid": query_result[x][2],
            "password": query_result[x][3],
            "company": query_result[x][1],
            "macid": query_result[x][4]
        }
        }
        result.update(temp)
    return query_result


@app.get("/GetAllUsersAsJson")
def getallusers():
    connection = StartUp()
    query_result = database.get_all_users(connection)
    result = {}
    for x in range(len(query_result)):
        temp = {query_result[x][0]: {
            "uuid": query_result[x][2],
            "password": query_result[x][3],
            "company": query_result[x][1],
            "macid": query_result[x][4]
        }
        }
        result.update(temp)
    return result


@app.get("/UpdateApp")
def update():
    return run_subprocess("git stash")+run_subprocess("git pull")


@app.get("/VersionNumber")
def version():
    return run_subprocess("git rev-parse --short HEAD")


@app.get("/DashboardSignIn")
def dashboardsignin(username: str, password: str):
    connection = StartUp()
    result = database.dashboard_signin(
        connection, username=username, password=password)
    return result


@app.get("/DashboardSignUp")
def dashboardsignup(username: str, password: str, secretkey: str):
    connection = StartUp()
    result = database.dashboard_signup(
        connection, username=username, password=password, secretkey=secretkey)
    return {"result": result}


@app.get("/RegisterUser")
def registeruser(company: str, uuid: str, password: str, macid: str):
    connection = StartUp()
    result = database.register_user(
        connection, company=company, uuid=uuid, password=password, macid=macid)
    return result


@app.get("/RegisterCompany")
def registercompany(company: str):
    connection = StartUp()
    result = database.register_company(
        connection, company=company)
    return result


@app.get("/GetAllCompanies")
def getallcompanies():
    connection = StartUp()
    result = database.get_all_companies(
        connection)
    return result


@app.get("/DeleteUser")
def deleteruser(company: str, uuid: str):
    connection = StartUp()
    result = database.delete_user(
        connection=connection, company=company, uuid=uuid)
    return result


@app.get("/UserSignin")
def userSignin(uuid: str, password: str, company: str):
    connection = StartUp()
    result = database.check_if_user_exists(
        connection, uuid=uuid, password=password, company=company)
    return result

# battery data coming from the app


@app.get("/PushData")
def pushData(uuid: str, timestamp: str, data: str, macid: str):
    connection = StartUp()
    result = database.push_data(
        connection, uuid=uuid, timestamp=timestamp, data=data, macid=macid)
    return result

# battery data going to the app


@app.get("/GetData")
def getData(uuid: str,  macid: str, timestamp: str = ""):
    connection = StartUp()
    result = database.get_data(connection, uuid, timestamp, macid)
    return result


@app.get("/GetAllData")
def getAllData():
    connection = StartUp()
    result = database.get_all_data_2(connection)
    return result


@app.get("/DownloadData")
def DownloadData():
    connection = StartUp()
    result = database.download_data(connection)
    return FileResponse(result, media_type='application/octet-stream', filename="all_data.json")


@app.get("/ExcuteOnSQLite")
def getData(command: str, secretkey: str):
    connection = StartUp()
    result = database.excete_on_sqlite(connection, command, secretkey)
    return result


@app.get("/logs")
async def logs(secretkey: str):
    if (secretkey == os.getenv("SECRET_KEY")):
        return FileResponse('logs/app.log')
    else:
        return {"error": "unauthorized access"}


@app.get("/")
def home():
    connection = StartUp()
    return {"result": "Hello World", "app": "rethium backend"}


if "__main__" == __name__:
    uvicorn.run("app:app", host='0.0.0.0', port=8000,
                reload=True, debug=True, workers=3)
