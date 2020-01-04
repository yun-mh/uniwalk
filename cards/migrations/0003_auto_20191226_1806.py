# Generated by Django 2.2.5 on 2019-12-26 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_card_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='card_number',
        ),
        migrations.RemoveField(
            model_name='card',
            name='expiration_month',
        ),
        migrations.RemoveField(
            model_name='card',
            name='expiration_year',
        ),
        migrations.RemoveField(
            model_name='card',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='last_name',
        ),
        migrations.AddField(
            model_name='card',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]