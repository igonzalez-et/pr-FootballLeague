from django.shortcuts import render
from .models import Team, Match, Event
from django.db import models

def home(request):
    return render(request, 'leagueApp/home.html')

def results(request, league):
    matches = Match.objects.filter(home_team__league=league).order_by('date')
    return render(request, 'leagueApp/results.html', {'matches': matches})

def match_detail(request, match_id):
    match = Match.objects.get(id=match_id)
    events = Event.objects.filter(match=match)
    return render(request, 'leagueApp/match_detail.html', {'match': match, 'events': events})

def standings(request, league):
    teams = Team.objects.filter(league=league).order_by('-points', '-goal_difference', '-goals_for')
    return render(request, 'leagueApp/standings.html', {'teams': teams})

def top_scorers(request, league):
    players = Event.objects.filter(match__home_team__league=league, event_type='goal') \
        .values('player__name', 'player__team__name') \
        .annotate(num_goals=models.Count('id')) \
        .order_by('-num_goals')
    return render(request, 'leagueApp/top_scorers.html', {'players': players})