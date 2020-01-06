# Generated by Django 2.2.5 on 2020-01-05 14:01

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20191225_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'カテゴリー', 'verbose_name_plural': 'カテゴリー'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created',), 'verbose_name': '商品', 'verbose_name_plural': '商品'},
        ),
        migrations.AlterField(
            model_name='product',
            name='product_number',
            field=models.CharField(blank=True, default=products.models.create_product_code, max_length=40, null=True, verbose_name='番号'),
        ),
    ]