# Generated by Django 5.1.6 on 2025-04-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_member_membership_type_issuedbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
