# Generated by Django 3.2.15 on 2024-11-13 04:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0021_alter_application_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='graduation_year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2000, message='Enter a realistic graduation year.'), django.core.validators.MaxValueValidator(2035, message='Enter a realistic graduation year.')]),
        ),
    ]