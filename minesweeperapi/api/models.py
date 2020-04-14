from django.db import models
from django.contrib.auth.models import User


class MinesweeperUser(models.Model):
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=70, unique=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(MinesweeperUser, self).save(*args, **kwargs)
        if is_new:
            authuser = User(username=self.username, email=self.email, password=self.username)
            authuser.save()

    class Meta:
        ordering = ['id']


class MinesweeperGame(models.Model):
    user = models.ForeignKey('MinesweeperUser', on_delete=models.CASCADE)
    game_won = models.BooleanField(default=False)
    game_time = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " : " + str(self.game_time)

    class Meta:
        ordering = ['user']


"""
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']
"""
