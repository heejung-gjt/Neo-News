# Generated by Django 3.2.5 on 2021-07-11 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20210711_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(default=1625996243.3620093),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.TextField(null=True),
        ),
    ]
