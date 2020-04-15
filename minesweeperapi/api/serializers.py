from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MinesweeperGame, MinesweeperUser


class MinesweeperUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MinesweeperUser
        fields = ['id','first_name', 'last_name', 'username', 'email']

class MinesweeperGameSerializer(serializers.ModelSerializer):
    #userid = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = MinesweeperGame
        fields = ['id', 'user', 'game_time', 'game_won', 'date']
