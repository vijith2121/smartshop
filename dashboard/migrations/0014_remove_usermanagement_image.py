# Generated by Django 3.1.7 on 2021-07-03 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_profile_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermanagement',
            name='image',
        ),
    ]
