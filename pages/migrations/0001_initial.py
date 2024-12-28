# Generated by Django 5.1.4 on 2024-12-28 08:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("spaces", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Page",
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
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField(blank=True)),
                ("slug", models.SlugField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_public", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_pages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="modified_pages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "space",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pages",
                        to="spaces.space",
                    ),
                ),
            ],
            options={
                "unique_together": {("space", "slug")},
            },
        ),
        migrations.CreateModel(
            name="PageVersion",
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
                ("content", models.TextField(blank=True)),
                ("version_number", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="page_versions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="versions",
                        to="pages.page",
                    ),
                ),
            ],
            options={
                "ordering": ["page", "-version_number"],
                "unique_together": {("page", "version_number")},
            },
        ),
    ]
