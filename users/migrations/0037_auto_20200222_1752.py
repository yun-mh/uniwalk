# Generated by Django 2.2.5 on 2020-02-22 08:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_auto_20200222_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, validators=[django.core.validators.RegexValidator(code='invalid-number', message='数字や記号以外の文字で入力してください。', regex="[\\D',. -]")], verbose_name='first name'),
        ),
    ]
