# Generated by Django 2.2.5 on 2020-01-30 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feet', '0008_auto_20200130_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedFootImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foot_left', models.ImageField(upload_to='feet')),
                ('foot_right', models.ImageField(upload_to='feet')),
            ],
        ),
    ]
