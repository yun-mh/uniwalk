# Generated by Django 2.2.5 on 2020-01-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_auto_20191231_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
