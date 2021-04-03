from django.urls import path

from P2G import views

app_name = 'P2G'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('games/', views.GamesView.as_view(), name='games'),
    path('highscores/', views.HighscoresView.as_view(), name='highscores'),
    path('other_players/<username>/', views.ListOtherPlayersView.as_view(), name='otherPlayers'),
    path('play_random/', views.PlayRandomView.as_view(), name='playRandom'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<category_id>/', views.CategoryView.as_view(), name='show_category'),
    path('category/<category_id>/add_game/', views.AddGameView.as_view(), name='add_game'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('game/<game_id>/', views.GameView.as_view(), name='show_game'),
    path('suggest/', views.GameSuggestionView.as_view(), name='suggest'),
    path('like_game/', views.LikeGameView.as_view(), name='like_game'),
    path('go_to_game/', views.GoToGameView.as_view(), name='go_to_game'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='account'),
    path('friends/<username>/', views.FriendsView.as_view(), name='friends'),
    path('add_friend/', views.AddFriendView.as_view(), name='add_friend'),
    path('remove_friend/', views.RemoveFriendView.as_view(), name='remove_friend'),
    path('search_friends/', views.SearchFriendsView.as_view(), name='search_friends'),
    path('search_others/', views.SearchOthersView.as_view(), name='search_others'),
    path('group/<group_id>/<user_id>/', views.GroupView.as_view(), name='group'),
    path('group_add_message/', views.GroupAddMessageView.as_view(), name='group_add_message'),
    path('message_check/', views.MessageCheckView.as_view(), name='message_check'),
    path('group_update/', views.GroupUpdateView.as_view(), name='group_update'),
    path('new_group/<user_id>/<game_id>/', views.NewGroupView.as_view(), name='new_group'),
    path('groups/<user_id>/', views.GroupsView.as_view(), name='groups'),
    path('add_score/', views.AddScoreView.as_view(), name='add_score'),
    path('approve_score/', views.ApproveScoreView.as_view(), name='approve_score'),
    path('remove_score/', views.RemoveScoreView.as_view(), name='remove_score'),
]
