#!/bin/sh

set -e

# Ensure data directories exist
# mkdir -p /data/input /data/output

# Run the Python script
# chmod +x ./src/main.py
/usr/bin/python ./src/main.py

echo "Processing complete. Check /data/output for results."