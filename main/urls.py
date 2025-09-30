# William Keilsohn
# September 30 2025

# Import Packages
from django.urls import path
from . import views

# Declare Valriables
urlpatterns = [
    path("", views.index, name="index"),
]