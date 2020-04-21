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
    token = request._auth.key
    if request.method == 'GET':
        users = MinesweeperUser.objects.all()
        if(CHECK_MASTER_TOKEN(token)):
            serializer = MinesweeperUserSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)
        authuser = Token.objects.get(key=token).user
        print('User email: ' + authuser.email)
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
        serializer = MinesweeperUserSerializer(minesweeperuser)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print('New user email: ' + data['email'])
        serializer = MinesweeperUserSerializer(data=data)
        if serializer.is_valid() and CHECK_MASTER_TOKEN(token):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    try:
        user = MinesweeperUser.objects.get(pk=pk)
        token = request._auth.key
        authuser = Token.objects.get(key=token).user
        print('User email: ' + authuser.email)
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        if(user.id == minesweeperuser.id or CHECK_MASTER_TOKEN(token)):
            serializer = MinesweeperUserSerializer(user)
            return JsonResponse(serializer.data)
        return HttpResponse('{"detail": "You are not authorized to view this page"}', status=401)

    elif request.method == 'PUT':
        if not CHECK_MASTER_TOKEN(token):
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
    token = request._auth.key
    if request.method == 'GET':
        all_games = MinesweeperGame.objects.all()
        if(CHECK_MASTER_TOKEN(token)):
            serializer = MinesweeperGameSerializer(all_games, many=True)
            return JsonResponse(serializer.data, safe=False)

        authuser = Token.objects.get(key=token).user
        print('User email: ' + authuser.email)
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
        games = MinesweeperGame.objects.filter(user=minesweeperuser)
        serializer = MinesweeperGameSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        authuser = Token.objects.get(key=token).user
        data = JSONParser().parse(request)
        print('User email: ' + authuser.email)
        print('Game won: ' + str(data['game_won']))
        print('Game time: ' + format_time((data['game_time'])))
        data['user'] = MinesweeperUser.objects.get(email=authuser.email).id
        serializer = MinesweeperGameSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=401)


def format_time(millis):
    minutes = (millis // 60000)
    seconds = (millis / 1000) % 60
    return str(minutes) + " minutes : " + str(seconds) + " seconds"


@csrf_exempt
@api_view(['GET'])
def online_users(request, format=None):

    token = request._auth.key
    if request.method == 'GET':
        if(CHECK_MASTER_TOKEN(token)):
            online_users = MinesweeperUser.objects.filter(online=True)
            serializer = MinesweeperUserSerializer(online_users, many=True)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'content' : 'You are not authorized to view this page'}, safe=False)

@csrf_exempt
@api_view(['GET'])
def highscore_list(request, format=None):

    token = request._auth.key
    if request.method == 'GET':
        all_games = MinesweeperGame.objects.filter(game_won=True)
        if(CHECK_MASTER_TOKEN(token)):
            serializer = MinesweeperGameSerializer(all_games, many=True)
            return JsonResponse(serializer.data, safe=False)

        authuser = Token.objects.get(key=token).user
        print('User email: ' + authuser.email)
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
        games = MinesweeperGame.objects.filter(
            user=minesweeperuser, game_won=True)
        serializer = MinesweeperGameSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET', 'DELETE'])
def game_detail(request, pk, format=None):
    try:
        game = MinesweeperGame.objects.get(pk=pk)
        token = request._auth.key
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


@csrf_exempt
@api_view(['POST'])
def games_count(request, format=None):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data['email']
        if(email == 'all'):
            games_count = MinesweeperGame.objects.all().count()
            games_count_won = MinesweeperGame.objects.filter(game_won=True).count()
            games_count_lost = MinesweeperGame.objects.filter(game_won=False).count()
            content = {'games_count': games_count, 'games_won' : games_count_won, 'games_lost': games_count_lost}
            return JsonResponse(content)
        authuser = MinesweeperUser.objects.get(email=email)
        games_count_won = MinesweeperGame.objects.filter(user=authuser, game_won=True).count()
        games_count_lost = MinesweeperGame.objects.filter(user=authuser, game_won=False).count()
        games_count = MinesweeperGame.objects.filter(user=authuser).count()
        content = {'user_email': email, 'games_count': games_count, 'games_won' : games_count_won, 'games_lost': games_count_lost}
        return JsonResponse(content)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        minesweeperuser = MinesweeperUser.objects.get(email=user.email)
        print('User email: ' + user.email)
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
