#!/bin/bash


# Load in Some Random Transactions
./travis/load_mempool_trans.sh

# Process those transactions
./process_transactions.py -c ./travis/config_travis.ini -V 

# Test Database Arrival

# API Tests Here : 

