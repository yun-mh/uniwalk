# Generated by Django 2.2.5 on 2019-12-18 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
    ]