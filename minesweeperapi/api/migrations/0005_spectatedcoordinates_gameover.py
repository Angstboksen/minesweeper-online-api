# Generated by Django 2.1.5 on 2020-04-29 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200429_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='spectatedcoordinates',
            name='gameover',
            field=models.BooleanField(default=False),
        ),
    ]
