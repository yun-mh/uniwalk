# Generated by Django 2.2.5 on 2019-12-27 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_guest_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
