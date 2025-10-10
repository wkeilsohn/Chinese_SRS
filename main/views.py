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
from .forms import *

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

def study(request, username): # Re-Integrated 
    if request.method == 'GET':
        user_df = pd.DataFrame(list(User_Words.objects.all().values()))
        user_words = user_df[user_df["user_name"] == username]
        word_ls = user_words["meaning"].tolist()
        request.session['pos_words'] = word_ls
        user_words = check_if_need_to_study(user_df=user_words)
        if len(user_words) <= 0: # If there are no words to study, take the user to their dashboard.
            return redirect('user_dash', username=username) 
        else:
            for index, row in user_words.iterrows():
                ans_ls = create_answer_ls(word_ls, row["meaning"])
                ans_form = AnswerForm(ans_ls=ans_ls)
                word_dict = row.to_dict()
                word_dict.pop("last_studied")
                request.session["word"] = word_dict
                request.session['ans_ls'] = ans_ls
                # test_form = TestForm() # Testing Only
                context = {'ans_form':ans_form, 'word_char':row["word"], 'answers':ans_ls, 'user_name':username, 'page_name':"Study"}
                return render(request, 'main/study.html', context)
    elif request.method == 'POST':
        ans_ls = request.session.get('ans_ls', None)
        ans_data_raw = int(request.POST.get('answers'))
        word = request.session.get('word', None)
        answer = ans_ls[ans_data_raw - 1]
        word = update_study_terms(user_df=word, user_ans_val=answer)
        User_Words.objects.filter(user_name=username, word=word["word"]).update(last_studied=word["last_studied"], study_level=word["study_level"], incorect_times=word["incorect_times"])
        return redirect('study', username=username)
    else:
        return redirect('user_dash', username=username) # IDK, this is just for edge cases. 

# def word_results(request, username): # Display answer and return to study list.
#     word = request.session.get('word', None)
#     answer = request.session.get('answer', None)
#     word = update_study_terms(user_df=word, user_ans_val=answer)
#     User_Words.objects.filter(user_name=username, word=word["word"]).update(last_studied=word["last_studied"], study_level=word["study_level"], incorect_times=word["incorect_times"])
#     return redirect('study', username=username)

def user_dash(request, username):
    return HttpResponse(username)
