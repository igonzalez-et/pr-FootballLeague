from django.urls import path
from . import views

app_name = 'leagueApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('results/<str:league>/', views.results, name='results'),
    path('standings/<str:league>/', views.standings, name='standings'),
    path('top-scorers/<str:league>/', views.top_scorers, name='top_scorers'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
]