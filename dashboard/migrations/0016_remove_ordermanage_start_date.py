# Generated by Django 3.1.7 on 2021-07-04 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_ordermanage_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermanage',
            name='start_date',
        ),
    ]
