# Generated by Django 5.1.6 on 2025-05-24 05:31

import library.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_member_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='due_date',
            field=models.DateField(default=library.models.get_due_date),
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
