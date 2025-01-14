# Generated by Django 3.2.15 on 2024-03-01 16:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0015_alter_application_program"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="student_number",
            field=models.CharField(
                help_text="UofT Student Number",
                max_length=10,
                validators=[
                    django.core.validators.RegexValidator(
                        code="invalid_student_number",
                        message="UofT Student number must be exactly 10 digits",
                        regex="^\\d{10}$",
                    )
                ],
            ),
        ),
    ]
