# Generated by Django 5.0a1 on 2023-09-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog_v1", "0003_alter_post_slug_alter_postcomment_post_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="subtitle",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
