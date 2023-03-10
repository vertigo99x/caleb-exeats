# Generated by Django 3.2.4 on 2023-01-06 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_college_departments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('useraname', models.CharField(default='', max_length=255)),
                ('priority', models.IntegerField(default=3, max_length=255)),
                ('complaint', models.TextField(default='', max_length=500)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
