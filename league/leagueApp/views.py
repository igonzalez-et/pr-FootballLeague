from django.shortcuts import render, redirect
from .models import *
from django.db import models
from django import forms
from leagueApp.models import *

def home(request):
    return render(request, 'leagueApp/home.html')

def standings(request):
    teams = Team.objects.all().order_by('-points')
    return render(request, 'leagueApp/standings.html', {'teams':teams})

def results(request):
    matches = Match.objects.all()
    return render(request, 'leagueApp/results.html', {'matches': matches})

def match_detail(request, match_id):
    match = Match.objects.get(id=match_id)
    events = Event.objects.filter(match=match)
    return render(request, 'leagueApp/match_detail.html', {'match': match, 'events': events})

# def standings(request, league):
#     teams = Team.objects.filter(league=league).order_by('-points', '-goal_difference', '-goals_for')
#     return render(request, 'leagueApp/standings.html', {'teams': teams})

def top_scorers(request):
    players = Player.objects.all().order_by('-goals')[:10]
    return render(request, 'leagueApp/top_scorers.html', {'players': players})


# class MenuForm(forms.Form):
#     lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    
# def menu(request):
#     form = MenuForm()
#     if request.method == "POST":
#         form = MenuForm(request.POST)
#         if form.is_valid():
#             lliga = form.cleaned_data.get("lliga")
#             return redirect('classificacio',lliga.id)
#     return render(request, "home.html",{
#                     "form": form,
#             })

