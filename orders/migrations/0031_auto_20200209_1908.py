# Generated by Django 2.2.5 on 2020-02-09 10:08

import core.models
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0030_auto_20200209_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_city_orderer',
            field=models.CharField(default=1, max_length=40, verbose_name='市区町村(お届け先)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='address_detail_orderer',
            field=models.CharField(default=1, max_length=40, verbose_name='建物名・部屋番号(お届け先)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name_orderer',
            field=models.CharField(default=1, max_length=30, verbose_name='名(お届け先)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name_orderer_kana',
            field=models.CharField(default=1, max_length=30, verbose_name='名(カナ, お届け先)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name_orderer_kana',
            field=models.CharField(default=1, max_length=30, verbose_name='姓(カナ, お届け先)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number_orderer',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=15, region=None, verbose_name='電話番号(お届け先)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='postal_code_orderer',
            field=models.CharField(max_length=7, verbose_name='郵便番号(お届け先)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='prefecture_orderer',
            field=core.models.JPPrefectureField(max_length=2, verbose_name='都道府県(お届け先)'),
        ),
    ]
