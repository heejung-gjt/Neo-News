# Generated by Django 3.2.5 on 2021-07-23 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0044_alter_article_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1627025250.5287333),
        ),
    ]
