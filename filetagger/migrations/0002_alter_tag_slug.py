# Generated by Django 5.0.1 on 2024-01-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filetagger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
