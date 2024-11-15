#!/bin/bash

# Find the paths to npm and node dynamically
NPM_PATH=$(which npm)
NODE_PATH=$(which node)

# Check if npm and node are found, then run the commands
if [[ -z "$NPM_PATH" || -z "$NODE_PATH" ]]; then
  echo "npm or node not found. Please ensure they are installed."
  exit 1
fi

# Check if the OS is Linux before attempting to `cd`
if [[ "$(uname)" == "Linux" ]]; then
  # Only change directory if on Linux
  cd /var/www/historian || { echo "Directory /var/www/historian not found."; exit 1; }
fi

# Run the npm script in the background
"$NPM_PATH" run dev &

# Run the node server
"$NODE_PATH" server/server.js
