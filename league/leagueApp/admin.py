from django.contrib import admin
from .models import *

class TeamAdmin(admin.ModelAdmin):
    fields = ['name', 'city', 'league']
    list_display = ['name','city','league']
    list_filter = ['league']
    search_fields = ['name','league']

admin.site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    fields = ['team', 'name', 'number', 'position']
    list_display = ['team', 'name', 'number', 'position']
    list_filter = ['team', 'position']
    search_fields = ['team','name', 'position']

admin.site.register(Player, PlayerAdmin)