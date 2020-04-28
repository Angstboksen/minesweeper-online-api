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
from .serializers import MinesweeperUserSerializer, MinesweeperGameSerializer, SpectatedGameSerializer, SpectatedCoordinatesSerializer
from .models import MinesweeperGame, MinesweeperUser, SpectatedGame, SpectatedCoordinates
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
            users = []
            for user in online_users:
                specgame = list(SpectatedGame.objects.filter(user=user)).pop()
                users.append({'user':user.first_name, 'game': specgame.game_code})
            return JsonResponse(users, safe=False)
        return JsonResponse({'content': 'You are not authorized to view this page'}, safe=False)


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
            games_count_won = MinesweeperGame.objects.filter(
                game_won=True).count()
            games_count_lost = MinesweeperGame.objects.filter(
                game_won=False).count()
            content = {'games_count': games_count,
                       'games_won': games_count_won, 'games_lost': games_count_lost}
            return JsonResponse(content)
        authuser = MinesweeperUser.objects.get(email=email)
        games_count_won = MinesweeperGame.objects.filter(
            user=authuser, game_won=True).count()
        games_count_lost = MinesweeperGame.objects.filter(
            user=authuser, game_won=False).count()
        games_count = MinesweeperGame.objects.filter(user=authuser).count()
        content = {'user_email': email, 'games_count': games_count,
                   'games_won': games_count_won, 'games_lost': games_count_lost}
        return JsonResponse(content)


@csrf_exempt
@api_view(['GET', 'POST'])
def spectated_game(request, format=None):
    token = request._auth.key

    if request.method == 'GET':
        all_games = SpectatedGame.objects.all()
        print(token)
        if(CHECK_MASTER_TOKEN(token)):
            serializer = SpectatedGameSerializer(all_games, many=True)
            return JsonResponse(serializer.data, safe=False)

        authuser = Token.objects.get(key=token).user
        print('User email: ' + authuser.email)
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
        games = SpectatedGame.objects.filter(
            user=minesweeperuser)
        serializer = SpectatedGameSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        if CHECK_MASTER_TOKEN(token):
            data = JSONParser().parse(request)
            serializer = SpectatedGameSerializer(data=data)
            print(data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=500)
        return HttpResponse('{"detail": "You are forbidden from posting a new game"}', status=403)


@csrf_exempt
@api_view(['POST'])
def spectated_game_instance(request, format=None):
    token = request._auth.key
    data = JSONParser().parse(request)
    if request.method == 'POST':
        game_code = data['game_code']
        authuser = Token.objects.get(key=token).user
        print('User email: ' + authuser.email)
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
        games = SpectatedGame.objects.filter(
            user=minesweeperuser, game_code=game_code)
        serializer = spectatedGameSerializer(games, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def spectated_game_detail(request, slug, format=None):
    try:
        game = SpectatedGame.objects.get(game_code=slug)
        token = request._auth.key
        authuser = Token.objects.get(key=token).user
        print('User email: ' + authuser.email)
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
    except SpectatedGame.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        if(game.user.id == minesweeperuser.id or CHECK_MASTER_TOKEN(token)):
            serializer = SpectatedGameSerializer(game)
            return JsonResponse(serializer.data)
        return HttpResponse('{"detail": "You are not authorized to view this page"}', status=401)

    elif request.method == 'PUT':
        if not CHECK_MASTER_TOKEN(token):
            return HttpResponse('{"detail": "You are forbidden from editing this game"}', status=403)
        data = JSONParser().parse(request)
        serializer = SpectatedGameSerializer(game, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if(CHECK_MASTER_TOKEN(token)):
            game.delete()
            return HttpResponse(status=204)
        return HttpResponse('{"detail": "You are forbidden from deleting users"}', status=403)


@csrf_exempt
@api_view(['GET', 'POST'])
def spectated_coordinates(request, slug, format=None):
    token = request._auth.key
    authuser = Token.objects.get(key=token).user
    try:
        game = SpectatedGame.objects.get(game_code=slug)
    except SpectatedGame.DoesNotExist:
        return JsonResponse({'content': 'Game does not exist'})
    if request.method == 'GET':
        all_coords = SpectatedCoordinates.objects.filter(game=game)
        if(CHECK_MASTER_TOKEN(token)):
            serializer = SpectatedCoordinatesSerializer(all_coords, many=True)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'content': 'Not authorized'}, safe=False)

    elif request.method == 'POST':
        if not CHECK_MASTER_TOKEN(token):
            return HttpResponse('{"detail": "You are forbidden from adding coordinates to game"}', status=403)
        data = JSONParser().parse(request)
        data['game'] = game.id
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
        serializer = SpectatedCoordinatesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=401)


@csrf_exempt
@api_view(['POST', 'PUT', 'DELETE'])
def spectated_coorinates_detail(request, slug, format=None):
    try:
        token = request._auth.key
        authuser = Token.objects.get(key=token).user
        print('User email: ' + authuser.email)
        minesweeperuser = MinesweeperUser.objects.get(email=authuser.email)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        spectatedgame = SpectatedGame.objects.get(game_code=slug)
        x = data['x_coord']
        y = data['y_coord']
        try:
            coords = SpectatedCoordinates.objects.get(
                game=spectatedgame, x_coord=x, y_coord=y)
        except SpectatedCoordinates.DoesNotExist:
            return HttpResponse(status=404)
        if(coords.game.user.id == minesweeperuser.id or CHECK_MASTER_TOKEN(token)):
            serializer = SpectatedCoordinatesSerializer(coords)
            return JsonResponse(serializer.data)
        return HttpResponse('{"detail": "You are not authorized to view this page"}', status=401)

    elif request.method == 'PUT':
        if not CHECK_MASTER_TOKEN(token):
            return HttpResponse('{"detail": "You are forbidden from editing this game"}', status=403)
        data = JSONParser().parse(request)
        try:
            spectatedgame = SpectatedGame.objects.get(game_code=slug)
        except:
            HttpResponse(status=404)
            return
        x = data['x_coord']
        y = data['y_coord']
        data['game'] = spectatedgame.id
        try:
            coords = SpectatedCoordinates.objects.get(game=spectatedgame, x_coord=x, y_coord=y)
            serializer = SpectatedCoordinatesSerializer(coords, data=data)
        except SpectatedCoordinates.DoesNotExist:
            serializer = SpectatedCoordinatesSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if(CHECK_MASTER_TOKEN(token)):
            coords.delete()
            return HttpResponse(status=204)
        return HttpResponse('{"detail": "You are forbidden from deleting users"}', status=403)


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


@csrf_exempt
@api_view(['POST'])
def check_user_exist(request, format=None):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data['email']
        minesweeperuser = MinesweeperUser.objects.filter(email=email).count()
        if minesweeperuser > 0:
            return JsonResponse({'content': 'true'}, status=200)
        return JsonResponse({'content': 'false'}, status=200)
