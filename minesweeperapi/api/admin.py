from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from .models import MinesweeperUser, MinesweeperGame, MultiplayerGame

TokenAdmin.raw_id_fields = ['user']
admin.site.register(MinesweeperGame)
admin.site.register(MinesweeperUser)
admin.site.register(MultiplayerGame)