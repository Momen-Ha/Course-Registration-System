# Generated by Django 5.0.6 on 2024-05-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseApp', '0019_student_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
