# Generated by Django 3.2 on 2023-07-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0003_auto_20230707_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipyingredient',
            name='amount',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(help_text='Введите название ингридиента', max_length=256, verbose_name='Название ингредиентов'),
        ),
    ]
