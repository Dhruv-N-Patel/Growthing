# Generated by Django 4.2.2 on 2023-07-08 03:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appname", "0022_project_tools_roadmap_tools"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="emoji",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="roadmap",
            name="emoji",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
