from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from .models import Player, Game
from datetime import date
import whr


class IndexView(generic.ListView):
    template_name = 'elo/index.html'
    context_object_name = 'players'

    def get_queryset(self):
        return Player.objects.order_by('-elo')


class ProfileView(generic.DetailView):
    model = Player
    template_name = 'elo/profile.html'


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

    base = whr.Base(config={'w2': 300})
    games = Game.objects.order_by('game_date')
    start_date = date(2022, 5, 11)
    for game in games:
        base.create_game(game.black.name, game.white.name, game.result, (game.game_date - start_date).days)
    base.iterate(100)
    print(base.get_ordered_ratings())
    for player in players:
        player.elo = base.ratings_for_player(player.name)[-1][1]
        player.save()

    return HttpResponseRedirect(reverse('elo:index'))