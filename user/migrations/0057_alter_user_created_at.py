# Generated by Django 3.2.5 on 2021-08-09 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0056_alter_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(default=1628498536.641338),
        ),
    ]