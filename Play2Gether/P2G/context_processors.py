from P2G.models import Category, Game

def menu(request):
    games_list = Game.objects.all().order_by('-likes')[:5]
    category_list = Category.objects.all().order_by('-likes')[:5]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['games'] = games_list
        
    return context_dict