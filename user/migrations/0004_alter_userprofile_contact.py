# Generated by Django 5.1.5 on 2025-03-20 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_workerprofile_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='contact',
            field=models.IntegerField(blank=True),
        ),
    ]
