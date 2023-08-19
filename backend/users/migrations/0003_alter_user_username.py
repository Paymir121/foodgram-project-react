# Generated by Django 3.2 on 2023-07-04 13:19

import django.contrib.auth.validators
from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_auto_20230317_1409"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=150,
                unique=True,
                validators=[
                    django.contrib.auth.validators.ASCIIUsernameValidator(),
                    users.validators.validator_username,
                ],
            ),
        ),
    ]
