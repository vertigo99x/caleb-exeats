# Generated by Django 3.2.4 on 2022-10-24 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20221023_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='allusers',
            name='date_added_main',
            field=models.CharField(choices=[(0, 0), (1, 1), (2, 2)], default=2, max_length=255),
        ),
        migrations.AddField(
            model_name='events',
            name='date_added_main',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='forms',
            name='date_added_main',
            field=models.CharField(default='', max_length=255),
        ),
    ]
