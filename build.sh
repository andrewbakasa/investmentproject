#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- Building the project ---"

# 1. Install dependencies
python3.12 -m pip install -r requirements.txt

# 2. Run Migrations
echo "--- Running Database Migrations ---"
python3.12 manage.py migrate --noinput

# 3. Collect Static
echo "--- Processing Static Files ---"
# We use --no-post-process to ensure WhiteNoise doesn't crash 
# during the build if the manifest is acting up.
python3.12 manage.py collectstatic --noinput --no-post-process

echo "--- Build Completed Successfully ---"
# #!/bin/bash
# echo "Building the project..."
# python3.12 -m pip install -r requirements.txt
# echo "Make Migrations..."
# python3.12 manage.py makemigrations --noinput
# python3.12 manage.py migrate --noinput
# echo "Collect Static..."
# python3.12 manage.py collectstatic --noinput --clear