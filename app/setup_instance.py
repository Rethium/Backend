from os import path, mkdir,system

dirs = ["logs", "database", "public/downloads"]

for dir in dirs:
    if not path.exists(dir):
        mkdir(dir)

with open('logs/app.log', 'w+') as fp:
    fp.close()

system("git fetch --all")
system("git checkout --track origin/staging")