# Generated by Django 2.2.5 on 2020-01-17 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0021_auto_20200117_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='design',
            name='liner_color_left',
        ),
    ]