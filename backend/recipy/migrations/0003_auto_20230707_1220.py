# Generated by Django 3.2 on 2023-07-07 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0002_auto_20230706_1438'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients',
            new_name='Ingredient',
        ),
        migrations.RenameModel(
            old_name='RecipyIngredients',
            new_name='RecipyIngredient',
        ),
    ]