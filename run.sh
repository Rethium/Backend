#!/bin/bash
echo "Removing Old DOckerfile"
rm Dockerfile
echo "Downloading New DockerFIle"
wget https://raw.githubusercontent.com/Rethium/Backend/main/Dockerfile
echo "Building and running new container"
docker build --network=host -t rethium_backend .
docker run -d -p 8000:8000 rethium_backend
