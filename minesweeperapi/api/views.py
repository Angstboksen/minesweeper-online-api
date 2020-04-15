from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework import renderers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import MinesweeperUserSerializer, MinesweeperGameSerializer
from .models import MinesweeperGame, MinesweeperUser
from .permissions import IsOwnerOrReadOnly
from .mastertoken import CHECK_MASTER_TOKEN



@csrf_exempt
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'games': reverse('game-list', request=request, format=format)
    })

@csrf_exempt
@api_view(['GET', 'POST'])
def user_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    token = dict(request.headers)['Authorization'].split(' ')[1]
    if request.method == 'GET':
        users = MinesweeperUser.objects.all()
        if(CHECK_MASTER_TOKEN(token)):
            serializer = MinesweeperUserSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)
        authuser = Token.objects.get(key=token).user
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
        serializer = MinesweeperUserSerializer(minesweeperuser)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MinesweeperUserSerializer(data=data)
        if serializer.is_valid() and CHECK_MASTER_TOKEN(token):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user = MinesweeperUser.objects.get(pk=pk)
        token = dict(request.headers)['Authorization'].split(' ')[1]
        authuser = Token.objects.get(key=token).user
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        if(user.id == minesweeperuser.id or CHECK_MASTER_TOKEN(token)):
            serializer = MinesweeperUserSerializer(user)
            return JsonResponse(serializer.data)
        return HttpResponse('{"detail": "You are not authorized to view this page"}', status=401)

    elif request.method == 'PUT':
        if(user.id != minesweeperuser.id and not CHECK_MASTER_TOKEN(token)):
            return HttpResponse('{"detail": "You are forbidden from editing this user"}', status=403)
        data = JSONParser().parse(request)
        serializer = MinesweeperUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if(CHECK_MASTER_TOKEN(token)):
            user.delete()
            return HttpResponse(status=204)
        return HttpResponse('{"detail": "You are forbidden from deleting users"}', status=403)
        
    

@csrf_exempt
@api_view(['GET', 'POST'])
def game_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    token = dict(request.headers)['Authorization'].split(' ')[1]
    if request.method == 'GET':
        all_games = MinesweeperGame.objects.all()
        if(CHECK_MASTER_TOKEN(token)):
            serializer = MinesweeperGameSerializer(all_games, many=True)
            return JsonResponse(serializer.data, safe=False)
        
        authuser = Token.objects.get(key=token).user
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
        games = MinesweeperGame.objects.filter(user=minesweeperuser)
        serializer = MinesweeperGameSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        authuser = Token.objects.get(key=token).user
        data = JSONParser().parse(request)
        data['user'] = MinesweeperUser.objects.get(email=authuser.email).id
        serializer = MinesweeperGameSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'DELETE'])
def game_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        game = MinesweeperGame.objects.get(pk=pk)
        token = dict(request.headers)['Authorization'].split(' ')[1]
    except MinesweeperGame.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MinesweeperGameSerializer(game)
        return JsonResponse(serializer.data)
        
    elif request.method == 'DELETE':
        if(CHECK_MASTER_TOKEN(token)):
            game.delete()
            return HttpResponse(status=204)
        return HttpResponse('{"detail": "You are forbidden from deleting users"}', status=403)

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
