from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import renderers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import MinesweeperUserSerializer, MinesweeperGameSerializer
from .models import MinesweeperGame, MinesweeperUser
from .permissions import IsOwnerOrReadOnly



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class MinesweeperUserViewSet(viewsets.ModelViewSet):
 
    queryset = MinesweeperUser.objects.all()
    serializer_class = MinesweeperUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MinesweeperGameViewSet(viewsets.ModelViewSet):
 
    queryset = MinesweeperGame.objects.all()
    serializer_class = MinesweeperGameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

"""class HighscoreListViewSet(viewsets.ModelViewSet):
 
    queryset = HighscoreList.objects.all()
    serializer_class = HighscoreListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class HighscoreViewSet(viewsets.ModelViewSet):
 
    queryset = Highscore.objects.all()
    serializer_class = HighscoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]"""


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
