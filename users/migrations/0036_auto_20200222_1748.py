# Generated by Django 2.2.5 on 2020-02-22 08:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_auto_20200222_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, validators=[django.core.validators.RegexValidator(code='invalid-number', message='全角カタカナで入力してください。', regex='[\\D]')], verbose_name='first name'),
        ),
    ]
