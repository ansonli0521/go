from django.urls import path

from . import views

app_name = 'elo'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("result_input/", views.ResultInputView.as_view(), name="result_input"),
    path("elo_calculate/", views.elo_calculate, name="elo_calculate"),
    path("game_history/", views.GameHistoryView.as_view(), name="game_history"),
]