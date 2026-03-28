#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- Building the project ---"

# 1. Install dependencies
# Using -m pip is safer in shared environments
python3.12 -m pip install -r requirements.txt

# 2. Run Migrations
# Note: Ensure you have already committed migration files from your local machine
echo "--- Running Database Migrations ---"
python3.12 manage.py migrate --noinput

# 3. Collect Static
# This is the most important part for fixing your 'Missing Manifest' error
echo "--- Collecting Static Files ---"
python3.12 manage.py collectstatic --noinput --clear

echo "--- Build Completed Successfully ---"
# #!/bin/bash
# echo "Building the project..."
# python3.12 -m pip install -r requirements.txt
# echo "Make Migrations..."
# python3.12 manage.py makemigrations --noinput
# python3.12 manage.py migrate --noinput
# echo "Collect Static..."
# python3.12 manage.py collectstatic --noinput --clear