# Generated by Django 4.2.2 on 2023-06-22 11:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appname", "0002_project_tag"),
    ]

    operations = [
        migrations.CreateModel(
            name="Roadmap",
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
                ("project_name", models.CharField(max_length=255)),
                ("roadmap", models.TextField()),
            ],
        ),
    ]
