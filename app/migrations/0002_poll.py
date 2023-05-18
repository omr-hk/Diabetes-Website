# Generated by Django 4.2.1 on 2023-05-18 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("correct", models.PositiveIntegerField()),
                ("incorrect", models.PositiveBigIntegerField()),
            ],
        ),
    ]
