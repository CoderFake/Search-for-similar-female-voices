# Generated by Django 4.2.11 on 2024-06-09 07:37

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AudioFile",
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
                ("path", models.TextField()),
                ("faiss_index", models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
