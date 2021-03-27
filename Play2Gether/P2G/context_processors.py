from P2G.models import Category, Game

def menu(request):
    category_list = Category.objects.all().order_by('-likes')
    games_list = Game.objects.all().order_by('-likes')

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['games'] = games_list
        
    return context_dict