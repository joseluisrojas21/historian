#!/bin/bash
# Check if the OS is Linux before attempting to `cd`
if [[ "$(uname)" == "Linux" ]]; then
  # Only change directory if on Linux
  cd /var/www/historian || { echo "Directory /var/www/historian not found."; exit 1; }
fi

# Run the npm script in the background
npm run dev &

# Run the node server
node server/server.js
