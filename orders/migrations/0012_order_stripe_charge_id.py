# Generated by Django 2.2.5 on 2019-12-27 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20191225_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_charge_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
