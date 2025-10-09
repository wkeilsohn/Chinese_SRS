# William Keilsohn
# September 30

# Import Packages
from django.shortcuts import render, redirect
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
user_df = pd.DataFrame(list(User_Words.objects.all().values())) 

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

def study(request, username): # This May be broken up later... I just want to create the integration now. 
    user_df = pd.DataFrame(list(User_Words.objects.all().values()))
    user_words = user_df[user_df["user_name"] == username]
    word_ls = user_words["meaning"].tolist()
    request.session['pos_words'] = word_ls
    user_words = check_if_need_to_study(user_df=user_words)
    try:
        for index, row in user_words.iterrows():
            row_dict = row.to_dict()
            row_dict.pop("last_studied")
            request.session['word'] = row_dict
            return redirect('ask_word', username=username)
    except:
        return redirect('user_dash', username=username)

def ask_word(request, username): # How to handle an individual term... I think ...
    word = request.session.get('word', None)
    pos_words = request.session.get('pos_words', None)
    ans_ls = create_answer_ls(pos_words, word["meaning"])
    print(ans_ls)
    # Need to retrieve the answer from the web interface.
    context = {'word_char':word["word"], 'answers':ans_ls, 'user_name':username, 'page_name':"Study"}
    return render(request, 'main/study.html', context)

def word_results(request, username): # Display answer and return to study list.
    word = request.session.get('word', None)
    answer = request.session.get('answer', None)
    word = update_study_terms(user_df=word, user_ans_val=answer)
    User_Words.objects.filter(user_name=username, word=word["word"]).update(last_studied=word["last_studied"], study_level=word["study_level"], incorect_times=word["incorect_times"])
    return redirect('study', username=username)

def user_dash(request, username):
    return HttpResponse(username)
