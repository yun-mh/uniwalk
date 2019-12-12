# Generated by Django 2.2.5 on 2019-12-11 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0003_auto_20191202_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='title',
            field=models.CharField(default=1, max_length=20, verbose_name='デザイン名'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='design',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='design', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='design',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='design', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='image',
            name='back_left',
            field=models.ImageField(upload_to='designs', verbose_name='後面(左)'),
        ),
        migrations.AlterField(
            model_name='image',
            name='back_right',
            field=models.ImageField(upload_to='designs', verbose_name='後面(右)'),
        ),
        migrations.AlterField(
            model_name='image',
            name='bottom_left',
            field=models.ImageField(upload_to='designs', verbose_name='下面(左)'),
        ),
        migrations.AlterField(
            model_name='image',
            name='bottom_right',
            field=models.ImageField(upload_to='designs', verbose_name='下面(右)'),
        ),
        migrations.AlterField(
            model_name='image',
            name='design',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='designs.Design', verbose_name='デザインid'),
        ),
        migrations.AlterField(
            model_name='image',
            name='side_left',
            field=models.ImageField(upload_to='designs', verbose_name='側面(左)'),
        ),
        migrations.AlterField(
            model_name='image',
            name='side_right',
            field=models.ImageField(upload_to='designs', verbose_name='側面(右)'),
        ),
        migrations.AlterField(
            model_name='image',
            name='upper_left',
            field=models.ImageField(upload_to='designs', verbose_name='上面(左)'),
        ),
        migrations.AlterField(
            model_name='image',
            name='upper_right',
            field=models.ImageField(upload_to='designs', verbose_name='上面(右)'),
        ),
    ]
