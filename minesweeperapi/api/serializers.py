from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MinesweeperGame, MinesweeperUser, SpectatedGame, SpectatedCoordinates


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

class SpectatedGameSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = SpectatedGame
        fields = ['id', 'user', 'user_email', 'difficulty', 'game_time', 'date', 'game_code']
    
class SpectatedCoordinatesSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='game.user.email')
    game_code = serializers.ReadOnlyField(source='game.game_code')
    class Meta:
        model = SpectatedCoordinates
        fields = ['id', 'game', 'x_coord', 'y_coord','flagged', 'user', 'game_code', 'opened', 'bomb_count']

