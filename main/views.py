# William Keilsohn
# September 30

# Import Packages
from django.shortcuts import render
from django.http import HttpResponse

# Create Views

def index(request):
    return HttpResponse("Hello World!")