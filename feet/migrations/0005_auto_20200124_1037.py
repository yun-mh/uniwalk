# Generated by Django 2.2.5 on 2020-01-24 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feet', '0004_auto_20200122_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footsize',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー'),
        ),
    ]
