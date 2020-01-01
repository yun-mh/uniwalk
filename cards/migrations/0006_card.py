# Generated by Django 2.2.5 on 2019-12-31 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0005_delete_card'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(blank=True, max_length=50, null=True)),
                ('fingerprint', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
