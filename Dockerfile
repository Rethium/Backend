FROM ubuntu:focal

# installing software packages

RUN apt-get update
RUN apt-get install python3-pip -y
RUN apt-get install -y git
RUN apt-get install -y wget 
RUN apt-get install -y curl
RUN apt-get install vim nano -y
RUN apt-get update
RUN apt-get autoremove -y
RUN apt-get clean -y
RUN apt-get install --fix-missing

# setup project

WORKDIR /home/Rethium
RUN git clone https://github.com/Rethium/Backend
WORKDIR /home/Rethium/Backend
RUN git pull
RUN pip3 install uvicorn
RUN pip3 install pydantic
RUN pip3 install -r requirements.txt
RUN ls

EXPOSE 8000
CMD ["python3", "app.py"]