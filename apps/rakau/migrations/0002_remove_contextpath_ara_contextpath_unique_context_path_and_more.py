# Generated by Django 5.1 on 2024-08-25 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rakau", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="contextpath",
            name="ara_contextpath_unique_context_path",
        ),
        migrations.RenameIndex(
            model_name="contentnode",
            new_name="rakau_conte_content_fd14db_idx",
            old_name="ara_content_content_0516a9_idx",
        ),
        migrations.RenameIndex(
            model_name="contextpath",
            new_name="rakau_conte_parent__cff211_idx",
            old_name="ara_context_parent__c56010_idx",
        ),
        migrations.AlterField(
            model_name="contentnode",
            name="contextpath_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="rakau.contextpath",
            ),
        ),
        migrations.AlterField(
            model_name="contextfile",
            name="contextpath_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="rakau.contextpath",
            ),
        ),
        migrations.AlterField(
            model_name="contextpath",
            name="context_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="rakau.context",
            ),
        ),
        migrations.AlterField(
            model_name="contextpath",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="rakau.context",
            ),
        ),
        migrations.AlterField(
            model_name="contextroot",
            name="context_ptr",
            field=models.OneToOneField(
                auto_created=True,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="rakau.context",
            ),
        ),
        migrations.AlterField(
            model_name="contextroot",
            name="sites",
            field=models.ManyToManyField(through="rakau.SiteContext", to="sites.site"),
        ),
        migrations.AlterField(
            model_name="sitecontext",
            name="context_root",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="rakau.contextroot"
            ),
        ),
        migrations.AddConstraint(
            model_name="contextpath",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    ("parent__isnull", True), ("path__isnull", True), _negated=True
                ),
                fields=("path", "parent"),
                name="rakau_contextpath_unique_context_path",
                nulls_distinct=True,
            ),
        ),
    ]
