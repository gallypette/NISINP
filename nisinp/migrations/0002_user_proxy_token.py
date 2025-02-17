# Generated by Django 4.2.4 on 2023-08-28 12:17

from django.db import migrations, models
import nisinp.helpers


class Migration(migrations.Migration):

    dependencies = [
        ("nisinp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="proxy_token",
            field=models.CharField(
                default=nisinp.helpers.generate_token, max_length=255, unique=True
            ),
        ),
    ]
