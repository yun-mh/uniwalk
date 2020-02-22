# Generated by Django 2.2.5 on 2020-02-21 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0032_auto_20200209_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='length_left',
            field=models.DecimalField(decimal_places=0, max_digits=3, verbose_name='足長(左)'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='length_right',
            field=models.DecimalField(decimal_places=0, max_digits=3, verbose_name='足長(右)'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='width_left',
            field=models.DecimalField(decimal_places=0, max_digits=3, verbose_name='足幅(左)'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='width_right',
            field=models.DecimalField(decimal_places=0, max_digits=3, verbose_name='足幅(右)'),
        ),
    ]
