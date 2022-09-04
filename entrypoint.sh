#!/bin/bash

echo "Starting web server..."

npm --prefix web_app start &

echo "Starting python server..."

exec "$@"
