# Generated by Django 5.0.3 on 2024-04-04 20:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendances",
            name="break_end_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="attendances",
            name="break_start_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
