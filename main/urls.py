# William Keilsohn
# September 30 2025

# Import Packages
from django.urls import path
from . import views

# Declare Valriables
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:username>/", views.user_dash, name="user_dash"),
    path("<str:username>/study/", views.study, name="study"),
    # path("<str:username>/study/ask/", views.ask_word, name="ask_word"),
    # path("<str:username>/study/answer/", views.word_results, name="word_results"),
]