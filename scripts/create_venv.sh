#!/bin/bash

# Install tap-klaviyo in its own virtualenv
python3 -m venv ~/.virtualenv/tap-klaviyo
source ~/.virtualenv/tap-klaviyo/bin/activate
pip install tap-klaviyo
deactivate

# Install target-csv in its own virtualenv
python3 -m venv ~/.virtualenv/target-csv
source ~/.virtualenv/target-csv/bin/activate
pip install target-csv
deactivate

# Install target-postgres in its own virtual env
python3 -m venv ~/.virtualenv/target-postgres
source ~/.virtualenv/target-postgres/bin/activate
# Had to install this on Linux to bypass psycopg2 install error
#sudo apt-get install libpq-dev
pip install singer-target-postgres
deactivate

# Create temp folders to store CSV output
mkdir -p /tmp/klaviyo_output