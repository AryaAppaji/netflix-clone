# Generated by Django 5.1.4 on 2024-12-25 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authtoken", "0004_alter_tokenproxy_options"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExpiringToken",
            fields=[
                (
                    "token_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="authtoken.token",
                    ),
                ),
                (
                    "device",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("expires_at", models.DateTimeField()),
            ],
            bases=("authtoken.token",),
        ),
    ]