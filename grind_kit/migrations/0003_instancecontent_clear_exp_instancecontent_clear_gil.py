# Generated by Django 4.1.3 on 2022-11-21 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grind_kit', '0002_alter_instancecontent_required_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='instancecontent',
            name='clear_exp',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='instancecontent',
            name='clear_gil',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
