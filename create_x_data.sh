#!/bin/bash

curl -X POST 127.0.0.1:5000/shutdown
python main.py &
sleep 4
python create_x_data.py $1