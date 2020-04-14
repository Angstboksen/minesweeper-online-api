from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from .models import MinesweeperUser, MinesweeperGame

TokenAdmin.raw_id_fields = ['user']
admin.site.register(MinesweeperGame)
admin.site.register(MinesweeperUser)