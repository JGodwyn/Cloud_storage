# Generated by Django 3.0.5 on 2020-07-10 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0005_files'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='files',
            options={'verbose_name_plural': 'Files'},
        ),
        migrations.AlterField(
            model_name='files',
            name='size',
            field=models.DecimalField(decimal_places=5, max_digits=900),
        ),
    ]