#!/bin/bash

curl -X POST 127.0.0.1:5000/shutdown
sleep 2
python main.py &
/usr/local/bin/py.test main_system_test.py -v --junitxml=position.xml