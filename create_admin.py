import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_Management.settings')
django.setup()

from django.contrib.auth.models import User

# Your actual superuser details
username = "Krishna"
email = "imks9219@gmail.com"
password = "Kris1235"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created.")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")
