#!/bin/bash

# Log
touch travis/api.log

# Start API (And send it to background).
./api.py -c ./travis/config_travis.ini > travis/api.log  &

api_pid=$!

if [[ -e /proc/${api_pid} ]] ; then 
	echo -e "API Running with PID of ${api_pid}"
else 
	echo -e "API Crashed or is no longer running."
	exit 1
fi

