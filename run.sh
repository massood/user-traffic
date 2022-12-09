#!/usr/bin/env bash

# STAT_DEBUG="--debug"
HOST=0.0.0.0
PORT=5000

exec flask --app main $STAT_DEBUG run --host=$HOST --port=$PORT
