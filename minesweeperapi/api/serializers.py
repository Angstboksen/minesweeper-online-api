from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MinesweeperGame, MinesweeperUser, MultiplayerGame, MultiplayerCoordinates


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

class MultiplayerGameSerializer(serializers.ModelSerializer):
    player_one_email = serializers.ReadOnlyField(source='player_one.email')
    player_two_email = serializers.ReadOnlyField(source='player_two.email')
    game_winner_email = serializers.ReadOnlyField(source='game_winner.email')
    
    class Meta:
        model = MultiplayerGame
        fields = ['id', 'player_one', 'player_one_email', 'player_two', 'player_two_email', 'difficulty', 'game_winner', 'game_winner_email', 'game_winner_time', 'date', 'game_code']
    
class MultiplayerCoordinatesSerializer(serializers.ModelSerializer):
    player_email = serializers.ReadOnlyField(source='player.email')

    class Meta:
        model = MultiplayerCoordinates
        fields = ['id', 'game', 'x_coord', 'y_coord', 'player', 'player_email', 'flagged']

