#!/usr/bin/env bash
# build.sh

echo "=== Building Selva Clinic ==="

# Install dependencies
pip install -r requirements.txt

# Navigate to project directory
cd selvaclinic

# Collect static files
python manage.py collectstatic --noinput

echo "=== Build completed ==="