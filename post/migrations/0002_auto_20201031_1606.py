# Generated by Django 3.1.2 on 2020-10-31 16:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='picture'),
        ),
    ]
