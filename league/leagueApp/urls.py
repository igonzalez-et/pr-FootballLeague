from django.urls import path
from . import views

app_name = 'leagueApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('clasificacion/<int:league_id>/', views.standings, name='clasificacion'),
    path('goleadores/', views.top_scorers, name='goleadores'),
    path('resultados/', views.results, name='resultados'),
    path('menu/', views.menu, name='menu'),
    path('crear_liga/', views.crear_liga, name='crear_liga'),
    path('crear_partido/', views.crear_partido, name='crear_partido'),
    path('crear_partido/<int:league_id>', views.escoger_equipos_partido, name='escoger_equipos_partido'),
]