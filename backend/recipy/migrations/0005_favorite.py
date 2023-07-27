# Generated by Django 3.2 on 2023-07-20 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipy', '0004_auto_20230708_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='recipy.recipy', verbose_name='Избранное')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to=settings.AUTH_USER_MODEL, verbose_name='Избраник')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'unique_together': {('recipy', 'user')},
            },
        ),
    ]
