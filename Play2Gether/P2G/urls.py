from django.urls import path
from P2G import views

app_name = 'P2G'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('account/', views.account, name='account'),
    path('friends/', views.friends, name='friends'),
    path('games/', views.games, name='games'),
    path('groups/', views.groups, name='groups'),
    path('highscores/', views.highscores, name='highscores'),
    path('other_players/', views.otherPlayers, name='otherPlayers'),
    path('play_random/', views.playRandom, name='playRandom'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
