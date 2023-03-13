from django.urls import path
from . import views

app_name = 'leagueApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('clasificacion/', views.standings, name='clasificacion'),
    path('goleadores/', views.top_scorers, name='goleadores'),
    path('resultados/', views.results, name='resultados'),
]