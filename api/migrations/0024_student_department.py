# Generated by Django 3.2.4 on 2022-10-24 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_alter_allusers_forms_left'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='department',
            field=models.CharField(default='', max_length=255),
        ),
    ]
