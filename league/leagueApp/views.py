from django.shortcuts import render, redirect
from .models import *
from django.db import models
from django import forms
from leagueApp.models import *


def home(request):
    return render(request, 'leagueApp/home.html')

def standings(request, league_id=None):
    league = League.objects.get(pk=league_id)
    # teams = Team.objects.all().order_by('-points')
    teams = league.team_set.all().order_by('-points')
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


     
class EscogerLigaForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=League.objects.all())
    
def menu(request):
    form = EscogerLigaForm()
    if request.method == "POST":
        form = EscogerLigaForm(request.POST)
        if form.is_valid():
            liga = form.cleaned_data.get("lliga")
            return redirect('../clasificacion/'+str(liga.id))
    return render(request, "leagueApp/menu.html",{
                    "form": form,
            })

class LigaForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ['name']
   
def crear_liga(request):
    form = LigaForm()
    message = ""

    if request.method == 'POST':
        form = LigaForm(request.POST)
        if form.is_valid():
            nombre_liga = form.cleaned_data.get("name")
            if League.objects.filter(name = nombre_liga):
                message = "El nombre de la liga ya existe."
            else:
                message = "Se ha creado correctamente."
                form.save()

    return render(request, 'leagueApp/crear_liga.html', {'form': form, 'message': message})

   
def crear_partido(request):
    form = EscogerLigaForm()
    message = ""

    if request.method == 'POST':
        form = LigaForm(request.POST)
        if form.is_valid():
            liga = form.cleaned_data.get("lliga")
            return redirect('escoger_equipos_partido',liga.id)

    return render(request, 'leagueApp/crear_partido.html', {'form': form, 'message': message})


class EscogerEquiposPartidoForm():
    class Meta:
        model = Match
        fields = ['home_team','away_team']

def escoger_equipos_partido(request,league_id):
    lliga = League.objects.get(pk=league_id)
    form = EscogerEquiposPartidoForm()
    message = ""

    if request.method == "POST":
        form = EscogerEquiposPartidoForm(request.POST)
        if form.is_valid():
            equipo_local = form.cleaned.get("home_team")
            equipo_visitante = form.cleaned.get("away_team")

            if equipo_local != equipo_visitante:
                partido = Match()
                partido.home_team = equipo_local
                partido.away_team = equipo_visitante
                partido.league = lliga

                if Match.objects.filter(home_team = equipo_local, away_team = equipo_visitante, league = lliga):
                    message = "El partido ya existe"
                else:
                    partido.save()
            else:
                message = "Tienen que ser equipos diferentes."
    return render(request, 'leagueApp/crear_partido.html', {'form': form, 'message': message})


