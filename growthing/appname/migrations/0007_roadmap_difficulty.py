# Generated by Django 4.2.2 on 2023-06-25 21:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appname", "0006_project_difficulty"),
    ]

    operations = [
        migrations.AddField(
            model_name="roadmap",
            name="difficulty",
            field=models.CharField(
                choices=[
                    ("easy", "Easy"),
                    ("moderate", "Moderate"),
                    ("tough", "Tough"),
                ],
                default="misc",
                max_length=20,
            ),
        ),
    ]
