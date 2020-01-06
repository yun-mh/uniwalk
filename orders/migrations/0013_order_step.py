# Generated by Django 2.2.5 on 2020-01-05 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_stripe_charge_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='orders.Step', verbose_name='対応状況'),
        ),
    ]