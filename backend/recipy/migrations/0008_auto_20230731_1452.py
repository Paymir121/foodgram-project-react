# Generated by Django 3.2 on 2023-07-31 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0007_auto_20230727_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='slug',
        ),
    ]
