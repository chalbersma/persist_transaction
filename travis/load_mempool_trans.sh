#!/bin/bash

# Load Test Transaction

for transaction in $(curl -s https://blockchain.info/unconfirmed-transactions?format=json | jq '.txs[].hash' | tr -s '"' ' ' | xargs); do
	echo ${transaction}
	curl -Ls localhost:8080/api/addtrans/${transaction}
done

# Add DB Test Information Here
