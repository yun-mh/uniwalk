# Generated by Django 2.2.5 on 2019-12-13 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20191213_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='created',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated',
        ),
    ]