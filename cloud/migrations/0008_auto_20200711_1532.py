# Generated by Django 3.0.5 on 2020-07-11 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0007_folder_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='size',
            field=models.DecimalField(decimal_places=2, max_digits=900),
        ),
    ]
