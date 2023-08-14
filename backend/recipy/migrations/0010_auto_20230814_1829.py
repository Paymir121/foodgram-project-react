# Generated by Django 3.2 on 2023-08-14 15:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0009_merge_0007_auto_20230730_1143_0008_auto_20230731_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipy.recipy', verbose_name='Избранное'),
        ),
    ]
