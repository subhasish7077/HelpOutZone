# Generated by Django 4.2.5 on 2023-11-09 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("QandA", "0004_alter_tag_options_remove_question_views_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="QandA.question",
            ),
        ),
        migrations.AlterField(
            model_name="answer",
            name="votes",
            field=models.ManyToManyField(
                related_name="ans_votes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="votes",
            field=models.ManyToManyField(
                related_name="Ques_votes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tags",
                to="QandA.tagcategory",
            ),
        ),
    ]
