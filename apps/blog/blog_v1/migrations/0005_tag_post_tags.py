# Generated by Django 5.0a1 on 2023-10-05 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog_v1", "0004_post_subtitle"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.SlugField(max_length=32, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(to="blog_v1.tag"),
        ),
    ]
