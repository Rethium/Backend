FROM ubuntu:focal

# installing software packages

RUN apt-get update
RUN apt-get install python3-pip -y
RUN apt-get install -y git
RUN apt-get install -y wget 
RUN apt-get install -y curl
RUN apt-get install vim nano -y
# RUN apt install -y libprotobuf-dev protobuf-compiler
# RUN DEBIAN_FRONTEND=noninteractive apt-get -y install cmake 
# RUN apt-get install -y libopenblas-dev 
# RUN apt-get install -y liblapack-dev 
# RUN apt-get install -y libjpeg-dev

# installing python packages

# RUN pip3 install --upgrade pip
# RUN pip3 install flask-restful
# RUN pip3 install numpy==1.19.3
# RUN pip3 install dnspython==2.2.1
# RUN pip3 install itsdangerous==2.0.1

# Handing opencv dependencies

# RUN apt-get update
# RUN apt-get install ffmpeg -y

# remove unwanted packages

RUN apt-get autoremove -y
RUN apt-get clean -y

# setup project

WORKDIR /home/Rethium
RUN git clone https://github.com/Rethium/Backend
WORKDIR /home/Rethium/Backend
RUN git pull
RUN pip3 install uvicorn
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "app:app --reload"]