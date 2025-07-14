import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_Management.settings')
django.setup()

from django.contrib.auth.models import User

# Change these details to your desired new login
username = "Krishna"
email = "krishnashukla8687@gmail.com"
password = "Kris1236"

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.email = email
    user.save()
    print(f"✅ Password for '{username}' reset successfully.")
except User.DoesNotExist:
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser '{username}' created.")
