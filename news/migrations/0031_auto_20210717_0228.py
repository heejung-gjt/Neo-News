# Generated by Django 3.2.5 on 2021-07-17 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0030_auto_20210717_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1626488897.6802847),
        ),
        migrations.AlterField(
            model_name='article',
            name='ref',
            field=models.URLField(),
        ),
    ]
