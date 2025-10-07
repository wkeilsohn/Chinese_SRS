# William Keilsohn
# September 30

# Import Packages
from django.shortcuts import render
from django.http import HttpResponse
from .models import Hanzi, User_Words
import pandas as pd
from .study.study import *
from .study.time_manager import *
import numpy as np
import os
import warnings

## Manage Warnings
warnings.simplefilter("ignore")

# Load Initial Data
hanzi_df = pd.DataFrame(list(Hanzi.objects.all().values()))
user_df = df = pd.DataFrame(list(User_Words.objects.all().values())) 

# Create Views

def index(request):
    global hanzi_df
    global user_df
    user_name = str(input("What is your name: ")) # Temporary. Change to web page later. 
    check_val = check_existing_users(user_name=user_name, user_db=user_df, hanzi_df=hanzi_df)
    try:
        if check_val >= 1:
            pass
    except:
        for index, row in check_val.iterrows():
            user_word = User_Words(user_name = row["User_Name"], word = row["word"], meaning = row["meaning"], sheet_level = row["sheet_level"], last_studied = row["Last_Studied"], study_level = row["Study_Level"], word_level = row["Word_Level"], incorect_times = row["Inccorect_Times"])
            user_word.save()
    print(User_Words.objects.all().values())
    return HttpResponse("Hello World!")

def question(request, word):
    return HttpResponse(word)

def answer(request, meaning):
    return HttpResponse(meaning)

def user_dash(request, username):
    return HttpResponse(username)

