# Generated by Django 5.0.6 on 2024-05-16 21:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseApp', '0006_alter_courseschedule_endtime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='scheduleID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courseApp.courseschedule'),
        ),
    ]