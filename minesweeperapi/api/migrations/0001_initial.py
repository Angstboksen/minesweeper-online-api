# Generated by Django 2.1.5 on 2020-04-19 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MinesweeperGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_won', models.BooleanField(default=False)),
                ('game_time', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('difficulty', models.CharField(default='easy', max_length=45)),
            ],
            options={
                'ordering': ['user', 'game_won', 'game_time'],
            },
        ),
        migrations.CreateModel(
            name='MinesweeperUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(max_length=70, unique=True)),
                ('online', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='minesweepergame',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.MinesweeperUser'),
        ),
    ]
