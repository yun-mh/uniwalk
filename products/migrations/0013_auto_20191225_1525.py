# Generated by Django 2.2.5 on 2019-12-25 06:25

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20191224_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_number',
            field=models.CharField(blank=True, default=products.models.create_product_code, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='商品番号'),
        ),
    ]
