import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Play2Gether.settings')

import django
django.setup()
from django.utils import timezone
from django.contrib.auth.models import User
from P2G.models import Game, Category, UserProfile, Score, Group

def populate():
    card_games = [{'name': 'Solitaire',
                   'link': 'https://www.solitr.com/',
                   'description': 'Battle the card deck with strategic moves, to show of your logical thinking'},
                  {'name': 'Uno',
                   'link': 'https://www.letsplayuno.com',
                    'description': 'Show your friends who is the real king in uno ;)'},
                  {'name': 'Skat',
                   'link': 'https://www.playok.com/en/skat/',
                   'description': 'Call the right game and count the cards to beat your friends'}]

    classic_games = [{'name': 'Chess',
                      'link': 'https://chess24.com/en',
                      'description': 'The good old classic'},
                     {'name': 'MineSweeper',
                      'link': 'https://www.classicgamesarcade.com/deutsch/game/21649/minesweeper.html',
                      'description': 'Combine the numbers to detect all the mines'}]

    board_games = [{'name': 'Monopoly',
                    'link': 'https://www.gamepix.com/de/play/monopoly',
                    'description': 'Show your inner capitalist and become the richest player in the game'},
                   {'name': 'The Settlers',
                    'link': 'https://playclassic.games/games/real-time-strategy-dos-games-online/play-the-settlers-online/',
                    'description': 'Build your village, grow it a city and build your empire'}]

    other_games = [{'name': 'Skribbl.io',
                    'link': 'https://skribbl.io/',
                   'description': 'Discover your inner picasso, and make good guesses to beat your friends'},
                   {'name': 'AmongUs',
                    'link': 'https://www.gamepix.com/de/play/among-us',
                   'description': 'Finish your task or just find the murder in the group, or are you the impostor'},
                   {'name': 'Doodle Jump',
                    'link': 'https://gameforge.com/en-US/littlegames/doodle-jump/',
                    'description': 'Reach new spheres and get as high as you can'},
                   {'name': 'Slither.io',
                    'link': 'https://http://slither.io',
                    'description': 'Grow your snake and become the biggest, but watch out that you are not get eaten up...'}]

    action_games = [{'name': 'Fortnite',
                     'link': 'https://www.epicgames.com/fortnite/en-US/download',
                    'description': 'Can you survive longer than your friends?'},
                    {'name': 'Doom',
                     'link': 'https://www.classicgamesarcade.com/deutsch/game/21692/doom.html',
                     'description': 'Can you make it out of the hell?'}
                    ]

    cats = {'Card Games': {'games': card_games,
                           'description': 'A collection of all the card games you love'},
            'Classic Games': {'games': classic_games,
                              'description': 'A collection of good all classics that everyone knows'},
            'Board Games': {'games': board_games,
                            'description': 'Play your favorite board games online here :)'},
            'Action Games': {'games': action_games,
                             'description': 'Here you find the action and the thrill!'},
            'Other Games': {'games': other_games,
                            'description': 'If you can find your favorite game you might find it in this collection of unique games'},
            }

    user_profiles = [{'name': 'Niklas',
                     'bio': 'Hey there, I am Nik and always looking for an exciting match'},
                     {'name': 'John',
                      'bio': '20, passionate Fortnite player from Down Under '},
                     {'name': 'Kathrin',
                      'bio': 'Secretary from the US, always open for a nice chat'},
                     {'name': 'Richard',
                      'bio': 'Scientist searching for intellectual opponents'},
                     {'name': 'Hugo',
                      'bio': 'Retired Police officer with skat experience'},
                     {'name': 'Malte',
                      'bio': 'Passionate fisher and Norway fan'},
                     {'name': 'Naomi',
                      'bio': 'I Love Tennis'},
                     {'name': 'Toni',
                      'bio': 'The best thing in live are friends and good pasta'},
                     {'name': 'Charlotte',
                      'bio': 'Always in for fun game!!!'},
                     ]

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['description'])
        for g in cat_data['games']:
            add_game(c, g['name'], g['link'], g['description'])

    for c in Category.objects.all():
        for g in Game.objects.filter(category=c):
            print(f'-{c}:{g}')

    for p in user_profiles:
        add_user(p['name'], p['bio'])

    for p in UserProfile.objects.all():
        print(f'-{p}')

    for game in Game.objects.all():
        maxScore = random.randint(1000, 10000)
        n_scores = random.randint(0, 10)
        group = Group.objects.get_or_create(game=g, name=g.name)[0]
        group.save()
        for i in range(n_scores):
            #https://stackoverflow.com/questions/22816704/django-get-a-random-object
            ids = User.objects.values_list('id', flat=True)
            random_id = random.choice(ids)
            user = User.objects.get(id=random_id)
            group.users.add(user)
            score = random.randint(0, maxScore)
            approved = random.choice([True, False])
            date = timezone.now()
            add_score(game, user, score, approved, date, group)


def add_score(game, user, score, approved, date, group):
    s = Score.objects.get_or_create(user=user, score=score, date=date, game=game, group=group)[0]
    s.approved = approved
    s.save()
    return s


def add_user(name, bio):
    u = User.objects.get_or_create(username=name)[0]
    u.save()
    p = UserProfile.objects.get_or_create(user=u)[0]
    p.bio = bio
    p.save()
    return p


def add_cat(name, description):
    c = Category.objects.get_or_create(name=name)[0]
    c.description = description
    c.likes = random.randint(0, 1000)
    c.save()
    return c


def add_game(cat, name, link, description):
    play_count = random.randint(0,1000)
    likes = int(play_count * random.random())
    g = Game.objects.get_or_create(category=cat, name=name)[0]
    g.link = link
    g.description = description
    g.play_count = play_count
    g.likes = likes
    g.save()
    return g


if __name__ == '__main__':
    print('Starting P2G population script...')
    populate()

