# Generated by Django 3.2.13 on 2023-06-11 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0007_hss_test_users"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="project_description",
            field=models.CharField(max_length=500, null=True),
        ),
    ]