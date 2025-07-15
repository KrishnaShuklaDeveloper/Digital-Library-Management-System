#!/bin/bash

set -o errexit  # Exit immediately on error

# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py migrate --noinput

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Create superuser if not exists
if [ -f create_admin.py ]; then
  python create_admin.py
else
  echo "⚠️ Skipping superuser creation. create_admin.py not found."
fi

# 5. Load books (optional and should be idempotent)
if [ -f load_books.py ]; then
  python load_books.py
else
  echo "⚠️ Skipping book loading. load_books.py not found."
fi
