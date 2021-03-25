import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse

from P2G.models import Category, Game, User, UserProfile, Group, Message, Score
from P2G.forms import CategoryForm, GameForm, UserProfileForm, GroupForm


def index(request):
    return render(request, 'P2G/index.html')


def about(request):
    return render(request, 'P2G/about.html')


def highscores(request):
    game_list = Game.objects.all()
    context_dict = {}
    context_dict['games'] = game_list
    game_counter = 0
    for game in game_list:
        score_list = Score.objects.filter(game=game).order_by('-score')[:10]
        context_dict[game.name] = score_list
        game_counter = game_counter + 1

    return render(request, 'P2G/highscores.html', context=context_dict)


class CategoriesView(View):
    def get(self, request):
        category_list = Category.objects.all().order_by('-likes')
        return render(request, 'P2G/categories.html', {'categories': category_list})


class GamesView(View):
    def get(self, request):
        games_list = Game.objects.all().order_by('-likes')
        return render(request, 'P2G/games.html', {'games': games_list})


class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'P2G/add_category.html', {'form': form})

    @method_decorator(login_required)
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
    @method_decorator(login_required)
    def get(self, request, category_id):
        if int(category_id) != -1:
            category = Category.objects.get(id=category_id)
            form = GameForm(initial={'category': category})
        else:
            form = GameForm()

        context_dict = {'form': form, 'category_id': category_id}
        return render(request, 'P2G/add_game.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, category_id):
        form = GameForm(request.POST)

        if form.is_valid():
            game = form.save(commit=True)
            return redirect(reverse('P2G:show_game', kwargs={'game_id': game.id}))
        else:
            print(form.errors)

        context_dict = {'form': form, 'category_id': category_id}
        return render(request, 'P2G/add_game.html', context_dict)


class GameView(View):
    def get(self, request, game_id):
        game = Game.objects.get(id=game_id)
        context_dict = {'game': game}
        context_dict['scores'] = Score.objects.filter(game=game).order_by('-score')[:5]
        return render(request, 'P2G/game.html', context_dict)


class GameSuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        games_query = Game.objects.all()
        games = []
        for game in games_query:
            if game.name.startswith(suggestion):
                games.append(game)

        return render(request, 'P2G/game-suggestion.html', {'games': games})


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

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('P2G:index'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'P2G/account.html', context_dict)

    @method_decorator(login_required)
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
    @method_decorator(login_required)
    def get(self, request, username):
        profiles = UserProfile.objects.all()
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        friends = user_profile.friends.all()
        return render(request, 'P2G/other_players.html', {'user_profile_list': profiles, 'friends': friends})


class AddFriendView(View):
    @method_decorator(login_required)
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
    @method_decorator(login_required)
    def get(self, request, username):
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        friends = user_profile.friends.all()
        return render(request, 'P2G/friends.html', {'friends': friends})


class RemoveFriendView(View):
    @method_decorator(login_required)
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
    @method_decorator(login_required)
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

        return render(request, 'P2G/others_list.html', {'user_profile_list': user_profile_list, 'friends': friends})


class GroupView(View):
    @method_decorator(login_required)
    def get(self, request, group_id, user_id):
        group = Group.objects.get(id=int(group_id))
        context_dict = {}
        context_dict['group_id'] = group_id
        context_dict['user_id'] = int(user_id)
        context_dict['users'] = []
        for user in group.users.all():
            context_dict['users'].append(user.user)
        context_dict['name'] = group.name
        context_dict['game'] = group.game
        context_dict['messages'] = Message.objects.filter(group=group).order_by('date')
        context_dict['scores'] = Score.objects.filter(group=group).order_by('-score')[:5]
        context_dict['approvals'] = Score.objects.filter(approved=False).exclude(user=user_id)
        return render(request, 'P2G/group.html', context=context_dict)


class GroupAddMessageView(View):
    @method_decorator(login_required)
    def get(self, request):
        group_id = request.GET['group_id']
        group = Group.objects.get(id=group_id)
        user_id = request.GET['user_id']
        user = User.objects.get(id=user_id)
        message = request.GET['message']
        Message.objects.create(sender=user, content=message, date=timezone.now(), group=group)
        messages = Message.objects.filter(group=group).order_by('date')
        return render(request, 'P2G/group_log.html', {'messages': messages})


class GroupUpdateView(View):
    @method_decorator(login_required)
    def get(self, request):
        group_id = int(request.GET['group_id'])
        group = Group.objects.get(id=group_id)
        messages = Message.objects.filter(group=group).order_by('date')
        return render(request, 'P2G/group_log.html', {'messages': messages})


class MessageCheckView(View):
    @method_decorator(login_required)
    def get(self, request):
        latest_client = int(request.GET['latest_message_id'])
        group_id = int(request.GET['group_id'])
        group = Group.objects.get(id=group_id)
        latest_server = Message.objects.filter(group=group).order_by('-date')[0].id

        if latest_client == latest_server:
            out = False
        else:
            out = latest_server
        return HttpResponse(out)


class NewGroupView(View):
    @method_decorator(login_required)
    def get(self, request, user_id, game_id):
        print(game_id)
        context_dict ={}
        if int(game_id) != -1:
            game = Game.objects.get(id=int(game_id))
            form = GroupForm(initial={'game': game})
        else:
            form = GroupForm()
        context_dict['form'] = form
        context_dict['user_id'] = int(user_id)
        context_dict['user_profile_list'] = UserProfile.objects.all()
        return render(request, 'P2G/new_group.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, user_id, game_id):
        user_ids = request.POST.get('users').split(',')
        user_ids.append(user_id)
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            for u_id in user_ids:
                user = User.objects.get(id=int(u_id))
                user_profile = UserProfile.objects.get(user=user)
                form.instance.users.add(user_profile)
            return redirect(reverse('P2G:group',
                                kwargs={'group_id': form.instance.id, 'user_id': user_id}))
        else:
            print(form.errors)
        return redirect(reverse('P2G:new_group',
                                kwargs={'user_id': user_id, 'game_id': game_id}))


class GroupsView(View):
    @method_decorator(login_required)
    def get(self, request, user_id):
        user = User.objects.get(id=int(user_id))
        user_profile = UserProfile.objects.get(user=user)
        groups = user_profile.group_set.all()

        group_collection = []
        for group in groups:
            dict = {}
            dict['group_id'] = group.id
            dict['name'] = group.name
            users = []
            for u in group.users.all():
                if u.user.id != int(user_id):
                    users.append(u.user.username)
            dict['users'] = users
            group_collection.append(dict)

        return render(request, 'P2G/groups.html', {'groups': group_collection, 'user_id': user_id})


class AddScoreView(View):
    @method_decorator(login_required)
    def get(self, request):
        group_id = int(request.GET['group_id'])
        group = Group.objects.get(id=group_id)

        if int(request.GET['user_id']) != -1:
            user_id = int(request.GET['user_id'])
            score = int(request.GET['score'])
            user = User.objects.get(id=user_id)
            date = timezone.now()
            game = group.game
            Score.objects.create(user=user, score=score, date=date, game=game, group=group)

        scores = Score.objects.filter(group=group).order_by('-score')[:5]
        return render(request, 'P2G/highscore_table.html', {'scores': scores})


class ApproveScoreView(View):
    @method_decorator(login_required)
    def get(self, request):
        user_id = int(request.GET['user_id'])
        if int(request.GET['score_id']) != -1:
            score_id = int(request.GET['score_id'])
            score = Score.objects.get(id=score_id)
            score.approved = True
            score.save()
        approvals = Score.objects.filter(approved=False).order_by('date').exclude(user=user_id)
        return render(request, 'P2G/approval_table.html', {'approvals': approvals})


class RemoveScoreView(View):
    @method_decorator(login_required)
    def get(self, request):
        score_id = int(request.GET['score_id'])
        user_id = int(request.GET['user_id'])
        Score.objects.filter(id=score_id).delete()
        approvals = Score.objects.filter(approved=False).order_by('date').exclude(user=user_id)
        return render(request, 'P2G/approval_table.html', {'approvals': approvals})


class PlayRandomView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        group = Group.objects.filter(randGroup=True)

        if len(group) == 0:
            games = Game.objects.all()
            index = random.randint(0,len(games)-1)
            game = games[index]
            name = 'Random Group Playing ' + game.name
            group = Group.objects.create(game=game, name=name, randGroup=True)
        else:
            group = group[0]
        group.users.add(user_profile)

        if group.users.count() >= 4:
            group.randGroup = False
            group.save()

        return redirect(reverse('P2G:group',
                                kwargs={'group_id': group.id, 'user_id': user_id}))
