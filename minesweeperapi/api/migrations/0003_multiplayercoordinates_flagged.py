# Generated by Django 2.1.5 on 2020-04-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200421_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplayercoordinates',
            name='flagged',
            field=models.BooleanField(default=False),
        ),
    ]
