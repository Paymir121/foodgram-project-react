# Generated by Django 3.2 on 2023-07-30 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_user',
        ),
    ]
