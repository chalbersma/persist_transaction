#!/bin/bash

# Install Electrum Dependencies
sudo apt-get install python-qt4 python-pip

# Install Electrum
sudo pip2 install ./travis/sources/Electrum-2.9.3.tar.gz

# Start Electrum Daemon
electrum -w ./travis/electrum/shitty_test_wallet daemon start

	# Note, the above uses a test wallet. That wallet
	# is not secure. Do not send transactions to addresses
	# in this wallet. Expect this wallet to be compromised
	# by default.

# Check to see if Electrum is doing it's thing righ
electrum is_synchronized
