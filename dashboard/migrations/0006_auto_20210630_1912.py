# Generated by Django 3.1.7 on 2021-06-30 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_productmanagement_final'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmanagement',
            name='final',
            field=models.IntegerField(max_length=100),
        ),
    ]
