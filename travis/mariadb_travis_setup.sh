#!/bin/bash

set -x

# Setup The MariaDB Stuff for testing
service mysql status

# Sets up database
# Sets up users persist & persist_perf with the default
# super duper insecure passwords.
cat setup/setup.sql | mysql 

