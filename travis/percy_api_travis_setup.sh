#!/bin/bash

# Start API (And send it to background).
./api.py -c ./travis/config_travis.ini  &

api_pid=$!

echo -e "API Running with PID of ${api_pid}"

