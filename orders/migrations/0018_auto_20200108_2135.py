# Generated by Django 2.2.5 on 2020-01-08 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_auto_20200106_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='products.Product', verbose_name='商品'),
        ),
    ]