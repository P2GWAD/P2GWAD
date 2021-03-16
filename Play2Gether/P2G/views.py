from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from P2G.models import Category, Game, User, UserProfile
from P2G.forms import CategoryForm, GameForm, UserProfileForm


def index(request):
    return render(request, 'P2G/index.html')


def about(request):
    return render(request, 'P2G/about.html')


def account(request):
    return render(request, 'P2G/account.html')


def friends(request):
    return render(request, 'P2G/friends.html')

def groups(request):
    return render(request, 'P2G/groups.html')


def highscores(request):
    return render(request, 'P2G/highscores.html')


def playRandom(request):
    return render(request, 'P2G/play_random.html')


class CategoriesView(View):
    def get(self, request):
        category_list = Category.objects.all().order_by('-likes')
        return render(request, 'P2G/categories.html', {'categories': category_list})


class GamesView(View):
    def get(self, request):
        games_list = Game.objects.all().order_by('-likes')
        return render(request, 'P2G/games.html', {'games': games_list})


class AddCategoryView(View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'P2G/add_category.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            cat = form.save(commit=True)
            return redirect(reverse('P2G:show_category',
                                    kwargs={'category_id': cat.id}))
        else:
            print(form.errors)

        return render(request, 'P2G/add_category.html', {'form': form})


class CategoryView(View):
    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        games = Game.objects.filter(category=category).order_by('-likes')
        context_dict={}
        context_dict['category'] = category
        context_dict['games'] = games
        return render(request, 'P2G/category.html', context=context_dict)


class AddGameView(View):
    def get(self, request, category_id):
        if int(category_id) != -1:
            category = Category.objects.get(id=category_id)
            form = GameForm(initial={'category': category})
        else:
            form = GameForm()

        context_dict = {'form': form, 'category_id': category_id}
        return render(request, 'P2G/add_game.html', context_dict)

    def post(self, request, category_id):
        form = GameForm(request.POST)

        if form.is_valid():
            game = form.save(commit=True)
            return redirect(reverse('P2G:show_category', kwargs={'category_id': game.category.id}))
        else:
            print(form.errors)

        context_dict = {'form': form, 'category_id': category_id}
        return render(request, 'P2G/add_game.html', context_dict)


class GameView(View):
    def get(self, request, game_id):
        game = Game.objects.get(id=game_id)
        context_dict = {'game': game}
        return render(request, 'P2G/game.html', context_dict)


def get_game_list(max_results=0, starts_with=''):
    game_list = []

    if starts_with:
        game_list = Game.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(game_list) > max_results:
            game_list = game_list[:max_results]

    return game_list


class GameSuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        game_list = get_game_list(max_results=10, starts_with=suggestion)

        if len(game_list) == 0:
            game_list = Game.objects.order_by('-likes')

        return render(request, 'P2G/game-suggestion.html', {'games': game_list})


def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('P2G:index'))
        else:
            print(form.errors)
    context_dict = {'form': form}
    return render(request, 'P2G/profile_registration.html', context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'bio': user_profile.bio,
                                'profile_image': user_profile.profile_image})
        return user, user_profile, form

    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('P2G:index'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'P2G/account.html', context_dict)

    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('P2G:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('P2G:account', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'P2G/account.html', context_dict)


class ListOtherPlayersView(View):
    def get(self, request, username):
        profiles = UserProfile.objects.all()
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        friends = user_profile.friends.all()
        return render(request, 'P2G/other_players.html', {'user_profile_list': profiles, 'friends': friends})


class AddFriendView(View):
    def get(self, request):
        user_id = int(request.GET['user_id'])
        friend_id = int(request.GET['friend_id'])
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        friend = User.objects.get(id=friend_id)
        friend_profile = UserProfile.objects.get(user=friend)
        user_profile.friends.add(friend_profile)
        return HttpResponse('Done')


class FriendsView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        friends = user_profile.friends.all()
        return render(request, 'P2G/friends.html', {'friends': friends})


class RemoveFriendView(View):
    def get(self, request):
        user_id = int(request.GET['user_id'])
        friend_id = int(request.GET['friend_id'])
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        friend = User.objects.get(id=friend_id)
        friend_profile = UserProfile.objects.get(user=friend)
        user_profile.friends.remove(friend_profile)
        friends = user_profile.friends.all()
        return render(request, 'P2G/friend_list.html', {'friends': friends})


class SearchFriendsView(View):
    def get(self, request):
        user_id = int(request.GET['user_id'])
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)

        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        friends_query = user_profile.friends.all()
        friends = []
        for friend in friends_query:
            if friend.user.username.startswith(suggestion):
                friends.append(friend)

        if len(friends) == 0:
            friends = user_profile.friends.all()

        return render(request, 'P2G/friend_list.html', {'friends': friends})


class SearchOthersView(View):
    def get(self, request):
        user_id = int(request.GET['user_id'])
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        friends = user_profile.friends.all()

        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        user_profiles = UserProfile.objects.all()
        user_profile_list = []
        for user_profile in user_profiles:
            if user_profile.user.username.startswith(suggestion):
                user_profile_list.append(user_profile)

        if len(user_profile_list) == 0:
            user_profile_list = UserProfile.objects.all()

        return render(request, 'P2G/others_list.html', {'user_profile_list': user_profile_list, 'friends':friends})