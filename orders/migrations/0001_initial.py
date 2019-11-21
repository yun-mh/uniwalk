# Generated by Django 2.2.5 on 2019-11-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name_orderer', models.CharField(max_length=30, verbose_name='姓()')),
                ('first_name_orderer', models.CharField(max_length=30, verbose_name='名()')),
                ('last_name_orderer_kana', models.CharField(max_length=30, verbose_name='姓(,カナ)')),
                ('first_name_orderer_kana', models.CharField(max_length=30, verbose_name='名(,カナ)')),
                ('email', models.CharField(max_length=254, verbose_name='メールアドレス')),
                ('phone_number_orderer', models.CharField(max_length=15, verbose_name='電話番号()')),
                ('postal_code_orderer', models.CharField(max_length=7, verbose_name='郵便番号()')),
                ('prefecture_orderer', models.CharField(max_length=2, verbose_name='都道府県()')),
                ('address_city_orderer', models.CharField(max_length=40, verbose_name='市区町村()')),
                ('address_detail_orderer', models.CharField(max_length=40, verbose_name='建物名・部屋番号()')),
                ('last_name_recipient', models.CharField(max_length=30, verbose_name='姓()')),
                ('first_name_recipient', models.CharField(max_length=30, verbose_name='名()')),
                ('last_name_recipient_kana', models.CharField(max_length=30, verbose_name='姓(,カナ)')),
                ('first_name_recipient_kana', models.CharField(max_length=30, verbose_name='名(,カナ)')),
                ('phone_number_recipient', models.CharField(max_length=15, verbose_name='電話番号()')),
                ('postal_code_recipient', models.CharField(max_length=7, verbose_name='郵便番号()')),
                ('prefecture_recipient', models.CharField(max_length=2, verbose_name='都道府県()')),
                ('address_city_recipient', models.CharField(max_length=40, verbose_name='市区町村()')),
                ('address_detail_recipient', models.CharField(max_length=40, verbose_name='建物名・部屋番号()')),
                ('order_date', models.DateTimeField(verbose_name='注文日時')),
                ('payment', models.CharField(max_length=2, verbose_name='支払方法')),
                ('amount', models.IntegerField(verbose_name='支払総額')),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_code', models.CharField(max_length=3)),
                ('step_name', models.CharField(max_length=20)),
            ],
        ),
    ]
