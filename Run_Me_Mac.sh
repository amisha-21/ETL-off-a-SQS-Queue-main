#!/bin/bash

#Run the docker-compose file
echo "Running docker-compose"
docker-compose up -d


#Run the Main.py file
echo "Executing Main.py"
Python3 Main/Main.py
echo "Completed"