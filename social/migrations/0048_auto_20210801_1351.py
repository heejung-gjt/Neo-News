# Generated by Django 3.2.5 on 2021-08-01 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0047_auto_20210801_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1627793519.4571447),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1627793519.4571447),
        ),
    ]
