from django.urls import path

from . import views

app_name = 'elo'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:player_id>/", views.profile, name="profile"),
    path("elo_calculation/", views.EloCalculationView.as_view(), name="elo_calculation"),
    path("elo_calculate/", views.elo_calculate, name="elo_calculate"),
    path("game_history/", views.GameHistoryView.as_view(), name="game_history"),
]