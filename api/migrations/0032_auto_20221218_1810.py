# Generated by Django 3.2.4 on 2022-12-18 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_forms_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AlterField(
            model_name='allusers',
            name='hostel',
            field=models.CharField(default='none', max_length=255),
        ),
        migrations.AlterField(
            model_name='allusers',
            name='usercat',
            field=models.CharField(choices=[('student', 'student'), ('porter', 'porter'), ('parent', 'parent'), ('saffairs', 'saffairs'), ('security', 'security')], max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='matric_no',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
