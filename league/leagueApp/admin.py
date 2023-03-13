from django.contrib import admin
from .models import *

class TeamAdmin(admin.ModelAdmin):
    fields = ['name', 'city', 'league', 'points', 'goal_difference', 'goals_for']
    list_display = ['name','city','league', 'points', 'goal_difference', 'goals_for']
    list_filter = ['league']
    search_fields = ['name','league']

admin.site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    fields = ['team', 'name', 'number', 'position', 'goals']
    list_display = ['team', 'name', 'number', 'position', 'goals']
    list_filter = ['team', 'position']
    search_fields = ['team','name', 'position']

admin.site.register(Player, PlayerAdmin)

class MatchAdmin(admin.ModelAdmin):
    fields = ['date', 'home_team', 'away_team', 'home_score', 'away_score']
    list_display = ['date', 'home_team', 'away_team', 'home_score', 'away_score']
    list_filter = ['date', 'home_team', 'away_team']
    search_fields = ['date', 'home_team', 'away_team']

admin.site.register(Match, MatchAdmin)