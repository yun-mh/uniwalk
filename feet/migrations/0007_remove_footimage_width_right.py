# Generated by Django 2.2.5 on 2020-01-30 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feet', '0006_footimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footimage',
            name='width_right',
        ),
    ]
