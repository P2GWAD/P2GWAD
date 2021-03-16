from django.shortcuts import render
from P2G.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect


def index(request):
    return render(request, 'P2G/index.html')

def about(request):
    return render(request, 'P2G/about.html')

def account(request):
    return render(request, 'P2G/account.html')

def friends(request):
    return render(request, 'P2G/friends.html')

def games(request):
    return render(request, 'P2G/games.html')

def groups(request):
    return render(request, 'P2G/groups.html')

def highscores(request):
    return render(request, 'P2G/highscores.html')

def otherPlayers(request):
    return render(request, 'P2G/other_players.html')

def playRandom(request):
    return render(request, 'P2G/play_random.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_image' in request.FILES:
                profile.picture = request.FILES['profile_image']
            profile.save()
            registered = True 
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'P2G/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST'
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('P2G:about'))
            else:
                print(f"Invalid login details: {username}, {password}")
                return HttpResponse("Invalid login details supplied.")
        else:
            return render(request, 'P2G/login.html')

