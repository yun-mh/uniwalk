# Generated by Django 2.2.5 on 2020-01-17 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0025_auto_20200117_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='down',
            field=models.ImageField(upload_to='designs', verbose_name='下面'),
        ),
        migrations.AlterField(
            model_name='image',
            name='front',
            field=models.ImageField(upload_to='designs', verbose_name='正面'),
        ),
        migrations.AlterField(
            model_name='image',
            name='side',
            field=models.ImageField(upload_to='designs', verbose_name='側面'),
        ),
        migrations.AlterField(
            model_name='image',
            name='up',
            field=models.ImageField(upload_to='designs', verbose_name='上面'),
        ),
    ]
