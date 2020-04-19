from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MinesweeperGame, MinesweeperUser


class MinesweeperUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MinesweeperUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'online']

class MinesweeperGameSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    user_name = serializers.ReadOnlyField(source='user.first_name')
    
    class Meta:
        model = MinesweeperGame
        fields = ['id', 'user', 'user_email', 'user_name', 'game_time', 'game_won', 'date', 'difficulty']
