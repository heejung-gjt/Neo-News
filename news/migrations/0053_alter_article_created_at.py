# Generated by Django 3.2.5 on 2021-08-01 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0052_alter_article_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1627787240.6133),
        ),
    ]