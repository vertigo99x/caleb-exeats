# Generated by Django 3.2.4 on 2022-10-26 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_alter_allusers_usercat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departments', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
