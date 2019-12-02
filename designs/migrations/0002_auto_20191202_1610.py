# Generated by Django 2.2.5 on 2019-12-02 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_auto_20191122_2328'),
        ('designs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='product_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product'),
        ),
        migrations.AddField(
            model_name='design',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='design',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='designs.Design', verbose_name='デザインid'),
            preserve_default=False,
        ),
    ]
