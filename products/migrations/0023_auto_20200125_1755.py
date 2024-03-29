# Generated by Django 2.2.5 on 2020-01-25 08:55

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20200124_1508'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': '商品イメージ', 'verbose_name_plural': '商品イメージ'},
        ),
        migrations.AlterModelOptions(
            name='template',
            options={'verbose_name': 'テンプレート', 'verbose_name_plural': 'テンプレート'},
        ),
        migrations.AlterField(
            model_name='template',
            name='midsole_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='ミッドソール(左)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='midsole_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='ミッドソール(右)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='outsole_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='アウトソール(左)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='outsole_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='アウトソール(右)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='shoelace_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='シューレス(左)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='shoelace_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='シューレス(右)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='tongue_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='タン(左)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='tongue_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='タン(右)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='upper_left',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='アッパーソール(左)'),
        ),
        migrations.AlterField(
            model_name='template',
            name='upper_right',
            field=models.FileField(blank=True, null=True, unique=True, upload_to=products.models.generate_path, verbose_name='アッパーソール(右)'),
        ),
    ]
