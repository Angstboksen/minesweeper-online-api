from .views import api_root, user_detail, user_list, game_list, game_detail, highscore_list, games_count
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', api_root),
    path('users/', user_list, name="user-list"),
    path('users/<int:pk>/', user_detail, name="user-detail"),
    path('games/', game_list, name="game-list"),
    path('games/<int:pk>/', game_detail, name="game-detail"),
    path('highscorelist/', highscore_list, name="highscore-list"),
    path('gamescount/', games_count, name="games-count" )
    
]

urlpatterns = format_suffix_patterns(urlpatterns)