# Generated by Django 3.0.5 on 2020-07-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=20000),
            preserve_default=False,
        ),
    ]
