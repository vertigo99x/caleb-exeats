# Generated by Django 3.2.4 on 2023-01-05 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20230101_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college', models.CharField(default='', max_length=255)),
                ('department', models.CharField(default='', max_length=255)),
            ],
        ),
    ]