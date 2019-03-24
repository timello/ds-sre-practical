#!/bin/bash

psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE USER entries WITH PASSWORD 'entries';
    CREATE DATABASE entries;
    GRANT ALL PRIVILEGES ON DATABASE entries TO entries;
EOSQL
