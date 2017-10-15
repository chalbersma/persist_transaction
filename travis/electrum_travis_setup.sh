#!/bin/bash

# Install Electrum Dependencies
sudo apt-get install python-qt4 python-pip

# Install Electrum
sudo pip2 install ./travis/sources/Electrum-2.9.3.tar.gz

# Create a Blank wallet
electrum create

# Start Electrum Daemon
electrum -w ./travis/shitty_test_wallet daemon start

# Check to see if Electrum is doing it's thing righ
electrum is_synchronized
