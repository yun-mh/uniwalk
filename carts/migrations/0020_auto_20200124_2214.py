# Generated by Django 2.2.5 on 2020-01-24 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0019_auto_20200124_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='design',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_items', to='designs.Design', verbose_name='デザイン'),
        ),
    ]
