# Generated by Django 2.2.5 on 2019-12-19 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0009_remove_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='更新日時'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='登録日時'),
        ),
    ]
