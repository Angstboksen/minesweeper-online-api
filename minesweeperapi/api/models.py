from django.db import models
from django.contrib.auth.models import User


class MinesweeperUser(models.Model):
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    online = models.BooleanField(default=False)

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
        return str(self.user) + " : " + self.difficulty + ' : ' + str(self.game_time) + ' : '+ str(self.game_won)  

    class Meta:
        ordering = ['user', 'difficulty', 'game_won', 'game_time']

class SpectatedGame(models.Model):
    user = models.ForeignKey('MinesweeperUser', on_delete=models.CASCADE)
    game_won = models.BooleanField(default=False)
    game_time = models.IntegerField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(default='easy', max_length=45)
    game_code = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return str(self.user) + " : " + self.difficulty + ' : ' + str(self.game_time) + ' : '+ str(self.game_won)  + ' : '+ str(self.game_code) + ' : ' + str(self.date)

    class Meta:
        unique_together = ['user', 'game_code']
        ordering = ['user', 'date']

class SpectatedCoordinates(models.Model):
    game = models.ForeignKey('SpectatedGame', on_delete=models.CASCADE, related_name="game", blank=True)
    x_coord = models.IntegerField(default=-1)
    y_coord = models.IntegerField(default=-1)
    flagged = models.BooleanField(default=False)
    bomb_count = models.IntegerField(default=-1)
    opened = models.BooleanField(default=False)
    gameover = models.BooleanField(default=False)

    def __str__(self):
        return str(self.game.game_code) + ' : ' + str(self.x_coord) + ' : ' + str(self.y_coord) + ' : ' + str(self.flagged) + ' : ' + str(self.gameover)
    
    class Meta:
        unique_together = ['game', 'x_coord', 'y_coord']
        ordering = ['game', 'gameover']

