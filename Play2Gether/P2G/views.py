from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from P2G.models import Category, Game
from P2G.forms import CategoryForm, GameForm


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


def otherPlayers(request):
    return render(request, 'P2G/other_players.html')


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