# Generated by Django 4.0.4 on 2022-06-12 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_favorite_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='name',
            field=models.CharField(default='Favorites', max_length=150),
        ),
    ]
