#!/usr/bin/env bash
# start.sh

echo "=== Starting Selva Clinic Application ==="

# Navigate to project directory
cd selvaclinic

# Set Python path to include current directory
export PYTHONPATH=/opt/render/project/src/selvaclinic:$PYTHONPATH

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn selvaclinic.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --pythonpath .