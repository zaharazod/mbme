# Generated by Django 5.0.7 on 2024-08-04 16:32

import awa.models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import functools
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("awa", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectlink",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                related_name="%(app_label)s_%(class)s_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="projectlink",
            name="icon",
            field=models.ImageField(
                blank=True,
                height_field="icon_height",
                null=True,
                upload_to=functools.partial(
                    awa.models.image_directory, *(), **{"role": "icons"}
                ),
                width_field="icon_width",
            ),
        ),
        migrations.AlterField(
            model_name="projectlink",
            name="modified_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                on_update=True,
                related_name="%(app_label)s_%(class)s_modified",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
