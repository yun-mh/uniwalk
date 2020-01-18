# Generated by Django 2.2.5 on 2020-01-17 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0014_auto_20200117_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='design',
            name='outsole_material_left',
        ),
        migrations.AddField(
            model_name='design',
            name='outsole_material_left',
            field=models.ManyToManyField(blank=True, null=True, related_name='designs', to='designs.Material'),
        ),
    ]