from django.urls import path
from .views import GameView
#from tamam_app.views import XboxGameListCreateView

app_name = "games"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    #path('games/', GameView.as_view()),
    #path('xbox_games/', XboxGameListCreateView.as_view(), name='xbox_games_list_create'),
    path('xbox_games/', GameView.as_view()),
]