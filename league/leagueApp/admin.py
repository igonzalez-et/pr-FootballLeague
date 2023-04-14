from django.contrib import admin
from django.db.models import Q
from .models import *

class LeagueAdmin(admin.ModelAdmin):
    fields = ['name']
    search_fields = ['name']
    
admin.site.register(League, LeagueAdmin)


class PlayerInline(admin.TabularInline):
    model = Player

class TeamAdmin(admin.ModelAdmin):
    fields = ['name', 'city', 'league', 'points', 'goal_difference', 'goals_for']
    list_display = ['name', 'city', 'league', 'points', 'goal_difference', 'goals_for']
    list_filter = ['league']
    search_fields = ['name', 'league']
    inlines = [PlayerInline]

admin.site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    fields = ['team', 'name', 'number', 'position', 'goals']
    list_display = ['team', 'name', 'number', 'position', 'goals']
    list_filter = ['team', 'position']
    search_fields = ['team', 'name', 'position']

admin.site.register(Player, PlayerAdmin)


class EventInline(admin.TabularInline):
    model = Event
    fields = ["time", "event_type", "player", "team"]
    ordering = ("time",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "player":
            match_id = request.resolver_match.kwargs['object_id']
            match = Match.objects.get(pk=match_id)
            # filtrar jugadores según los equipos que han jugado el partido
            kwargs["queryset"] = Player.objects.filter(team__in=[match.home_team, match.away_team])
        elif db_field.name == "team":
            match_id = request.resolver_match.kwargs['object_id']
            match = Match.objects.get(pk=match_id)
            # filtrar equipos según el partido seleccionado
            kwargs["queryset"] = Team.objects.filter(Q(name=match.home_team.name) | Q(name=match.away_team.name))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MatchAdmin(admin.ModelAdmin):
    search_fields = ["home_team", "away_team"]
    readonly_fields = ["home_score", "away_score"]
    list_display = ["home_team", "away_team", "home_score", "away_score"]
    inlines = [EventInline]

    def resultat(self, obj):
        gols_local = obj.event_set.filter(
            tipus=Event.EventType.GOL, equip=obj.local).count()
        gols_visit = obj.event_set.filter(
            tipus=Event.EventType.GOL, equip=obj.visitant).count()
        return "{} - {}".format(gols_local, gols_visit)


admin.site.register(Match, MatchAdmin)


class EventAdmin(admin.ModelAdmin):
    fields = ['match', 'team', 'player', 'event_type', 'time']
    list_display = ['match', 'team', 'player', 'event_type', 'time']
    list_filter = ['match']
    search_fields = ['match']

admin.site.register(Event, EventAdmin)