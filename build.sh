#!/bin/bash

# Install all requirements
pip install -r requirements.txt

# Run Django database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput


