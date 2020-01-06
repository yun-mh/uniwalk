# Generated by Django 2.2.5 on 2020-01-05 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_remove_order_cart'),
        ('carts', '0012_auto_20200105_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Order', verbose_name='注文'),
        ),
    ]
