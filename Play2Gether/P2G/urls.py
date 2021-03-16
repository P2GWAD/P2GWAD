from django.urls import path

from P2G import views

app_name = 'P2G'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('account/', views.account, name='account'),
    path('friends/', views.friends, name='friends'),
    path('games/', views.GamesView.as_view(), name='games'),
    path('groups/', views.groups, name='groups'),
    path('highscores/', views.highscores, name='highscores'),
    path('other_players/', views.otherPlayers, name='otherPlayers'),
    path('play_random/', views.playRandom, name='playRandom'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<category_id>/', views.CategoryView.as_view(), name='show_category'),
    path('category/<category_id>/add_game/', views.AddGameView.as_view(), name='add_game'),
    path('game/<game_id>/', views.GameView.as_view(), name='show_game'),
    path('suggest/', views.GameSuggestionView.as_view(), name='suggest'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
