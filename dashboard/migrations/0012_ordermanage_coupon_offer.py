# Generated by Django 3.1.7 on 2021-07-02 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_cartitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermanage',
            name='coupon_offer',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
