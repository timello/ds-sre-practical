#!/bin/sh

/usr/bin/mongorestore --archive < /docker-entrypoint-initdb.d/mongodb.dump
