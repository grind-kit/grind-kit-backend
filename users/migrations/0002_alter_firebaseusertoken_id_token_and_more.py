# Generated by Django 4.1.3 on 2023-07-27 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firebaseusertoken',
            name='id_token',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='firebaseusertoken',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
