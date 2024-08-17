# Generated by Django 5.1 on 2024-08-17 03:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tuhi", "0007_pagesection_created_pagesection_created_by_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pagesection",
            options={"verbose_name": "section"},
        ),
        migrations.AlterField(
            model_name="pagesection",
            name="page",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sections",
                to="tuhi.page",
            ),
        ),
    ]
