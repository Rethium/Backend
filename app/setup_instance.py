from os import path, mkdir

dirs = ["logs", "database"]

for dir in dirs:
    if not path.exists(dir):
        mkdir(dir)

with open('logs/app.log', 'w+') as fp:
    fp.close()