# Generated by Django 3.2.5 on 2021-07-22 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0036_auto_20210722_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1626969925.4473042),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1626969925.4473042),
        ),
    ]
