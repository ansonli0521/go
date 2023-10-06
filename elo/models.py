from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    elo = models.FloatField()

class Game(models.Model):
    black = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="black")
    white = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="white")
    result = models.CharField(max_length=1)
    game_date = models.DateField()