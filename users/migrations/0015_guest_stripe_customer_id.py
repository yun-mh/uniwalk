# Generated by Django 2.2.5 on 2019-12-27 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20191227_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]