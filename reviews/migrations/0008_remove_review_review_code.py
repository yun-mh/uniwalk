# Generated by Django 2.2.5 on 2020-01-25 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20200109_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='review_code',
        ),
    ]
