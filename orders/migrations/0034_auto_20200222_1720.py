# Generated by Django 2.2.5 on 2020-02-22 08:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0033_auto_20200221_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='first_name_orderer_kana',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator(code='invalid', message='全角カタカナで入力してください。', regex='[ア-ンー]')], verbose_name='名(カナ, お届け先)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name_recipient_kana',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='invalid', message='全角カタカナで入力してください。', regex='[ア-ンー]')], verbose_name='名(ご請求書先,カナ)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name_orderer_kana',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator(code='invalid', message='全角カタカナで入力してください。', regex='[ア-ンー]')], verbose_name='姓(カナ, お届け先)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name_recipient_kana',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(code='invalid', message='全角カタカナで入力してください。', regex='[ア-ンー]')], verbose_name='姓(ご請求書先,カナ)'),
        ),
    ]
