from elo.models import Player, Game
from datetime import date
import whr

base = whr.Base(config={'w2': 300})
players = Player.objects.all()
games = Game.objects.order_by('game_date')
start_date = date(2022, 5, 11)

for game in games:
    base.create_game(game.black.name, game.white.name, game.result, (game.game_date - start_date).days)
base.iterate(100)
print(base.get_ordered_ratings())
for player in players:
    print(player.name)
    player.elo = base.ratings_for_player(player.name)[-1][1]
    player.save()