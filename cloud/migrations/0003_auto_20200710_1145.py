# Generated by Django 3.0.5 on 2020-07-10 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0002_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
