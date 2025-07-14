#!/bin/bash

# Install all requirements
pip install -r requirements.txt

# Run Django database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create a superuser (only if it doesn't exist)
python create_admin.py

# Load books
python3 load_books.py
