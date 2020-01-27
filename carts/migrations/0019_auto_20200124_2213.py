# Generated by Django 2.2.5 on 2020-01-24 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0018_auto_20200119_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='design',
            field=models.ForeignKey(default=50, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='designs.Design', verbose_name='デザイン'),
            preserve_default=False,
        ),
    ]
