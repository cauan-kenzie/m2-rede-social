# Generated by Django 4.1 on 2022-08-28 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_follower_user_follow_follower_profile_uuid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, default="", max_length=255, null=True),
        ),
    ]