# Generated by Django 4.1.3 on 2023-03-20 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InstanceContent',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
    ]