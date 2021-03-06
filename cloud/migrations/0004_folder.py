# Generated by Django 3.0.5 on 2020-07-10 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0003_auto_20200710_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder', to='cloud.User')),
            ],
        ),
    ]
