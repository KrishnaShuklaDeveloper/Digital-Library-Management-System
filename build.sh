#!/bin/bash

# Install all requirements
pip install -r requirements.txt

# Run Django database migrations
python manage.py migrate --noinput

# (Optional) Collect static files if needed
python manage.py collectstatic --noinput
