# Generated by Django 2.2.5 on 2019-12-03 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_image_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='category',
        ),
    ]
