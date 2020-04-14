from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MinesweeperGame, MinesweeperUser


class MinesweeperUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MinesweeperUser
        fields = ['url', 'id','first_name', 'last_name', 'username', 'email']

class MinesweeperGameSerializer(serializers.HyperlinkedModelSerializer):
    userid = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = MinesweeperGame
        fields = ['url', 'id', 'user', 'userid', 'game_time', 'game_won', 'date']
