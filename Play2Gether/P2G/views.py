from django.shortcuts import render


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

