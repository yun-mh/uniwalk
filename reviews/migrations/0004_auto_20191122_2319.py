# Generated by Django 2.2.5 on 2019-11-22 14:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_auto_20191122_2319'),
        ('reviews', '0003_auto_20191122_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user_id',
        ),
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='商品'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
            preserve_default=False,
        ),
    ]
