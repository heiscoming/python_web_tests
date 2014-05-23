#!/bin/bash

curl -X POST 127.0.0.1:5000/shutdown
sleep 2
python main.py &
sleep 2
python create_x_data.py $1