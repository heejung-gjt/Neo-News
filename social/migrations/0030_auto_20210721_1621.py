# Generated by Django 3.2.5 on 2021-07-21 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0029_auto_20210721_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1626852114.5764267),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1626852114.5764267),
        ),
    ]
