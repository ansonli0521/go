from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.db.models import Q
from .models import Player, Game
from datetime import date
import whr


class IndexView(generic.ListView):
    template_name = 'elo/index.html'
    context_object_name = 'players'

    def get_queryset(self):
        return Player.objects.order_by('-elo')


def profile(request, player_id):
    player = Player.objects.get(pk=player_id)
    games = Game.objects.filter(Q(black=player) | Q(white=player)).order_by('-game_date')
    
    return render(request, 'elo/profile.html', {'player': player, 'games': games})

class ResultInputView(generic.ListView):
    template_name = 'elo/result_input.html'

    def get_queryset(self):
        return Player.objects.all()


class GameHistoryView(generic.ListView):
    template_name = 'elo/game_history.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.order_by('-game_date')


def elo_calculate(request):
    players = Player.objects.all()
    black_match = False
    white_match = False

    for player in players:
        if request.POST["black"] == player.name:
            black_match = True
        if request.POST["white"] == player.name:
            white_match = True
    if black_match == False:
        messages.info(request, 'No black player!')
        return HttpResponseRedirect(reverse('elo:result_input'))
    elif white_match == False:
        messages.info(request, 'No white player!')
        return HttpResponseRedirect(reverse('elo:result_input'))
    
    new_game = Game(
        black = Player.objects.get(name=request.POST["black"]),
        white = Player.objects.get(name=request.POST["white"]),
        result = request.POST["result"],
        game_date = request.POST["game_date"]
    )
    new_game.save()

    base = whr.Base(config={'w2': 30})
    games = Game.objects.order_by('game_date')
    start_date = date(2023, 1, 1)
    for game in games:
        base.create_game(game.black.name, game.white.name, game.result, (game.game_date - start_date).days)
    base.iterate(1)
    for player in players:
        player.elo = base.ratings_for_player(player.name)[-1][-1]
        player.save()

    return HttpResponseRedirect(reverse('elo:index'))