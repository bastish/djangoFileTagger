# Generated by Django 5.0.1 on 2024-01-12 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filetagger', '0004_alter_file_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.TextField(),
        ),
    ]