# Generated by Django 2.2.5 on 2020-01-14 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='midsole_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='midsole_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='outsole_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='outsole_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='shoelace_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='shoelace_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='tongue_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='tongue_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='uppersole_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
        migrations.AlterField(
            model_name='template',
            name='uppersole_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to='product_templates'),
        ),
    ]
