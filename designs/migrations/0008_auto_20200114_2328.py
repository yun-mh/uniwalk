# Generated by Django 2.2.5 on 2020-01-14 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0007_auto_20200114_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='design', to='users.Guest'),
        ),
        migrations.AlterField(
            model_name='design',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='design', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='design',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='design', to=settings.AUTH_USER_MODEL),
        ),
    ]
