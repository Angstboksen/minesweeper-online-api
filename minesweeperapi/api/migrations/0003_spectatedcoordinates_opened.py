# Generated by Django 2.1.5 on 2020-04-28 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_spectatedcoordinates_bomb_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='spectatedcoordinates',
            name='opened',
            field=models.BooleanField(default=False),
        ),
    ]
