from .views import  api_root, MinesweeperGameViewSet, MinesweeperUserViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', MinesweeperUserViewSet)
router.register(r'games', MinesweeperGameViewSet)
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

