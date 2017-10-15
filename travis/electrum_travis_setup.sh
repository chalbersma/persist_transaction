#!/bin/bash

# Install Electrum Dependencies
sudo apt-get install python-qt4 python-pip

# Install Electrum
sudo pip2 install ./travis/sources/Electrum-2.9.3.tar.gz

# Start Electrum Daemon
electrum daemon start

# Check to see if Electrum is doing it's thing right
electrum is_synchronized
