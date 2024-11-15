# Generated by Django 4.2.2 on 2023-07-04 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appname", "0013_alter_customuser_managers_customuser_bio"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={},
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="bio",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="date_joined",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_staff",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_superuser",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="last_name",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="user_permissions",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="username",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
