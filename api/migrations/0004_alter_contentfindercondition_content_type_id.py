# Generated by Django 4.1.3 on 2023-04-15 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_contentfindercondition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentfindercondition',
            name='content_type_id',
            field=models.IntegerField(null=True),
        ),
    ]