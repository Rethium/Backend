import os

if(os.path.exists("logs")):
    pass
else:
    os.mkdir("logs")

with open('logs/app.log', 'w+') as fp:
    fp.close()