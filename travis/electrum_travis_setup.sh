#!/bin/bash

set -x

# Install Electrum Dependencies
sudo apt-get install python-qt4 python-pip jq

# Install Electrum
sudo pip2 install ./travis/sources/Electrum-2.9.3.tar.gz

# Start Electrum Daemon

electrum daemon start

	# Note, the above uses a test wallet. That wallet
	# is not secure. Do not send transactions to addresses
	# in this wallet. Expect this wallet to be compromised
	# by default.

# Check to see if Electrum is doing it's thing righ
if [[ "$(electrum daemon status | jq '.connected')" == "true" ]] ; then
	# Electrum Connected Successfully
	echo -e "Electrum Daemon Setup and Running"

else
	echo -e "Electrum Daemon Not Working"
	electrum daemon status | jq '.'
	exit 1
fi
