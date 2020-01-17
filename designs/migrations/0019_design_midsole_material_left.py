# Generated by Django 2.2.5 on 2020-01-17 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0018_auto_20200117_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='midsole_material_left',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='midsole_material_left', to='designs.Material'),
        ),
    ]
