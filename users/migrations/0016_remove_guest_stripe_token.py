# Generated by Django 2.2.5 on 2019-12-27 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_guest_stripe_customer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='stripe_token',
        ),
    ]
