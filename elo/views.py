from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.db.models import Q
from .models import Player, Game
from datetime import date
from elo.generate_elo import calculate
from elo.generate_elo_egf import egf_calculate
from elo.elo_reset import reset
from elo.game_input import delete_all_games, game_input
from decimal import Decimal


class IndexView(generic.ListView):
    template_name = 'elo/index.html'
    context_object_name = 'players'

    def get_queryset(self):
        return Player.objects.order_by('-elo')


def profile(request, player_id):
    player = Player.objects.get(pk=player_id)
    games = Game.objects.filter(Q(black=player) | Q(white=player)).order_by('-game_date')
    
    return render(request, 'elo/profile.html', {'player': player, 'games': games})

class EloCalculationView(generic.ListView):
    template_name = 'elo/elo_calculation.html'

    def get_queryset(self):
        return Player.objects.all()


class GameHistoryView(generic.ListView):
    template_name = 'elo/game_history.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.order_by('-game_date')


def elo_calculate(request):
    reset()
    if request.POST['method'] == 'elo':
        calculate(float(request.POST['k']), float(request.POST['f']))
    else:
        egf_calculate(Decimal(request.POST['k']), Decimal(request.POST['f']))
    return HttpResponseRedirect(reverse('elo:index'))

def reset_games(request):
    delete_all_games()
    game_input()
    return HttpResponseRedirect(reverse('elo:index'))