# Generated by Django 2.2.5 on 2020-02-06 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0022_remove_cartitem_feet'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='length_left',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=4, verbose_name='足長(左)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='length_right',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=4, verbose_name='足長(右)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='width_left',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=4, verbose_name='足幅(左)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='width_right',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=4, verbose_name='足幅(右)'),
            preserve_default=False,
        ),
    ]