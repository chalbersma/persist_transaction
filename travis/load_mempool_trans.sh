#!/bin/bash

# Load Test Transaction

for transaction in $(curl -s https://blockchain.info/unconfirmed-transactions?format=json | jq '.txs[].hash' | tr -s '"' ' ' | xargs); do
	echo ${transaction}
	curl -Ls localhost:8080/api/addtrans/${transaction}
done

# Add DB Test Information Here
transactions=$(echo "select count(*) from trked_trans" | mysql -N longtrans)

if [[ ${transactions} -gt 0 ]] ; then 
	# It's okay this is what we want
	echo -e "Load Test Transactions Made it to DB count: ${transactions}"
else
	tail -n 20 travis/api.log
	echo -e "Something wrong with Transactions, not showing up with test transactions count: ${transactions}"
	exit 1
fi
