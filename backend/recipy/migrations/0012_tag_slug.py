# Generated by Django 3.2 on 2023-08-15 10:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0011_remove_tag_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=255, unique=True, verbose_name='URL'),
            preserve_default=False,
        ),
    ]
