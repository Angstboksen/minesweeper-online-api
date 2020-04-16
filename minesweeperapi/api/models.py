from django.db import models
from django.contrib.auth.models import User


class MinesweeperUser(models.Model):
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=70, unique=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(MinesweeperUser, self).save(*args, **kwargs)
        if is_new:
            authuser = User(username=self.username, email=self.email,
                            first_name=self.first_name, last_name=self.last_name)
            authuser.set_password(self.username)
            authuser.save()

    class Meta:
        ordering = ['id']


class MinesweeperGame(models.Model):
    user = models.ForeignKey('MinesweeperUser', on_delete=models.CASCADE)
    game_won = models.BooleanField(default=False)
    game_time = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(default='easy', max_length=45)

    def __str__(self):
        return str(self.user) + " : " + str(self.game_time) + " : " + self.difficulty

    class Meta:
        ordering = ['user']
