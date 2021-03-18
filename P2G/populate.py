import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'P2GWAD.settings')

import django
django.setup()
from P2G.models import Score, Game, Categories, User, Group

def populate():
    
    game_pages = [
        {'name': 'Skribbl.io',
         'link': 'https://skribbl.io/'},
        {'name': 'Fortnite',
         'link': 'https://www.epicgames.com/fortnite/en-US/download'},
        'name': 'Solitaire',
        'link': 'https://www.solitr.com/']

    
    gamers = {'Players': {'Player': game_pages, 'score': 0}}
    
    
    for game, game_data in games.items():
        g = add_game(game)
        for g in game_data['Games']:
            add_game(g, g['name'], g['link'])
            
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
            
            

def add_score(game, user, score, date):
    s = Score.objects.get_or_create(game=game, user=user, score=score, date=date)[0]
    s.game=game
    s.user=user
    s.score=score
    s.date=date
    s.save()
    return s

def add_game(category, name, link, play_count, likes):
    g = Game.objects.get_or_create(category=category, name=name, link, play_count=play_count, likes=likes)[0]
    g.save()
    return g

def add_category(name, likes):
    c = Categories.objects.get_or_create(name=name, likes=likes)
    c.save()
    return c

def add_user(games, groups, friends, name, email, profile_image, bio):
    u = User.objects.get_or_create(games=games, groups=groups, friends=friends, name=name,
                                   email=email, profile_image=profile_image, bio=bio)
    u.save()
    return u

def add_group(game, name):
    t = Group.objects.get_or_create(game=game, name=name)
    t.save()
    return t 

    
if __name__ == '__main__':
    print('Starting...')
    populate()