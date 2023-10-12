from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    elo = models.FloatField()
    total_games = models.IntegerField(default=0)
    status = models.CharField(max_length=200, default='new')

class Game(models.Model):
    black = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="black")
    white = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="white")
    handicap = models.IntegerField(default=0)
    result = models.CharField(max_length=1)
    game_date = models.DateField()
    black_old_elo = models.FloatField(default=0)
    black_new_elo = models.FloatField(default=0)
    white_old_elo = models.FloatField(default=0)
    white_new_elo = models.FloatField(default=0)