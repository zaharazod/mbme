# Generated by Django 5.1 on 2023-10-09 17:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mbme", "0002_alter_user_options_alter_user_table"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AlterModelTable(
            name="user",
            table="auth_user",
        ),
    ]
