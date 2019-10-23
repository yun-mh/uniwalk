# Generated by Django 2.2.5 on 2019-10-23 13:34

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20191023_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='生年月日'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', '男性'), ('female', '女性'), ('others', 'その他')], max_length=10, verbose_name='性別'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='電話番号'),
        ),
    ]
