# Generated by Django 4.1 on 2022-09-17 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0012_alter_allusers_approvedexeats_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="forms",
            name="level",
            field=models.CharField(default="", max_length=255),
        ),
    ]
