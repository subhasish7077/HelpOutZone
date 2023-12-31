# Generated by Django 4.2.5 on 2023-10-29 07:26

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="emailSent",
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
                (
                    "subject",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="subject"
                    ),
                ),
                ("to", models.EmailField(max_length=254, verbose_name="to")),
                ("cc", models.TextField(blank=True, null=True, verbose_name="CC")),
                ("body", ckeditor_uploader.fields.RichTextUploadingField()),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_sent",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="emailGenerationDB",
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
                ("prompt", models.TextField(verbose_name="prompt")),
                (
                    "subject",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="subject"
                    ),
                ),
                ("body", ckeditor_uploader.fields.RichTextUploadingField()),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "token_used",
                    models.IntegerField(default=0, verbose_name="Token used"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_generation",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="contentGenerationDB",
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
                ("prompt", models.TextField(verbose_name="prompt")),
                ("generated_content", models.TextField()),
                ("generated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "token_used",
                    models.IntegerField(default=0, verbose_name="Token used"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="content_generation",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["generated_at"],
            },
        ),
    ]
