# William Keilsohn
# September 26 2025

###
# This file essentially acts as the "Brain" of the SRS Program.
###

# Import Packages
import os
import numpy as np
import pandas as pd
from .time_manager import *
import math
from random import randint
from django.utils import timezone

# Declare Variables
hanzi_df = pd.DataFrame()  # This is temporary

# Define Functions
def get_first_words(hanzi_df):
    return hanzi_df.head(5)

def get_next_set(hanzi_df, last_word):
    current_loc = hanzi_df[hanzi_df["Word"] == last_word].index[0]
    start_loc = current_loc + 1
    end_loc = start_loc + 5
    return hanzi_df.iloc[start_loc:end_loc]


def build_user_data(username, starting_words, word_level=1):
    tmp_df = starting_words
    tmp_df["User_Name"] = username
    tmp_df["Last_Studied"] = datetime.now()
    tmp_df["Study_Level"] = "PP"
    tmp_df["Word_Level"] = word_level
    tmp_df["Incorect_Times"] = 0
    return tmp_df

def check_existing_users(user_name, user_db, hanzi_df):
    try:
        user_df = user_db[user_db["User_Name"] == user_name]
        present_val = 1
    except:
        starting_words = get_first_words(hanzi_df=hanzi_df)
        user_df = build_user_data(username=user_name, starting_words=starting_words)
        present_val = user_df
    return present_val


def check_word_level(user_df):
    current_level = user_df.tail(1)["Word_Level"].iloc[0]
    new_level = current_level + 1
    return new_level


def add_new_user_words(hanzi_df, user_df):
    user_info = user_df.tail(1)
    user_name = user_info["User_Name"].iloc[0]
    last_word = user_info["Word"].iloc[0]
    new_words = get_next_set(hanzi_df=hanzi_df, last_word=last_word)
    new_word_level = check_word_level(user_df=user_df)
    user_words = build_user_data(
        username=user_name, starting_words=new_words, word_level=new_word_level
    )
    total_words = pd.concat([user_df, user_words], ignore_index=True)
    return total_words


def update_SRS_level(inc_times, study_level, inc_value):  # Return the new SRS Level
    global time_dict
    inc_adjust = math.ceil(inc_times / 2)
    c_stage = list(time_dict).index(study_level)
    if inc_value == 0:
        level_change = c_stage + 1
    else:
        c_adjust = 1
        if c_stage >= 5:
            c_adjust = 2
        level_change = math.floor(c_stage - (inc_adjust * c_adjust))
    if level_change < 0:  # I wish I had 0 wishes
        level_change = 0  # Granted. You now have 255 wishes.
    new_level = list(time_dict.keys())[level_change]
    # print(new_level)
    return new_level


def study_word(user_word_input, word_def_val):
    if word_def_val != user_word_input:
        return 1
    else:
        return 0

def create_answer_ls(word_ls, answer):
    indxs = [randint(0, len(word_ls)) for x in range(3)]
    indxs = [x - 1 if x >= len(word_ls) else x for x in indxs]
    ans = [word_ls[x] for x in indxs]
    y = randint(0, len(ans))
    ans.insert(y, answer)
    return ans


def create_answer_options(answer_ls):
    answer_df = pd.DataFrame(answer_ls)
    return answer_df


def check_if_need_to_study(user_df):
    global format_string
    no_need_to_study = []
    for index, row in user_df.iterrows():
        try:
            last_study_date = row["last_studied"]
        except:
            last_study_date = timezone.now()  # Error only occurs when crearing new user.
        time_since_studied = calculate_time_since_last_study(last_review_time=last_study_date)
        study_needed = check_if_study(p_val=row["study_level"], review_time=time_since_studied)
        if not study_needed:
            no_need_to_study.append(index)
    user_df.drop(no_need_to_study, inplace=True)
    return user_df

def update_study_terms(user_df, user_ans_val): # user_df is actually a dict
    ## Most of this function is a re-structure of the above one. 
    user_df["last_studied"] = datetime.now()
    study_result = study_word(user_ans_val, user_df["meaning"]) # Need to check the answer
    inc_val = user_df["incorect_times"] + study_result
    user_df["incorect_times"] = inc_val
    user_df["study_level"] = update_SRS_level(inc_times=inc_val, study_level=user_df["study_level"], inc_value=study_result)
    return user_df

def check_for_user_progress(user_df):
    global time_dict
    user_progress = user_df["Study_Level"].tolist()
    passing_level = list(time_dict.keys())[-4:]
    passed_words = []
    for i in user_progress:
        if i in passing_level:
            passed_words.append(i)
        else:
            pass
    if len(passed_words) >= math.ceil(3 * (len(user_progress) / 4)):
        return True
    else:
        return False


def user_advance(hanzi_df, user_df):
    user_status = check_for_user_progress(user_df=user_df)
    if user_status == True:
        user_df = add_new_user_words(hanzi_df=hanzi_df, user_df=user_df)
        check_if_need_to_study(
            user_df=user_df
        )  # Forces the user to study the new words.
    return user_df

def pre_process_choices(values):
    value_choices = []
    for i in range(1, len(values)+1):
            value_choices.append((i, values[i-1]))
    return value_choices

def stat_preper(df): 
    p_ls = []
    pp_ls = []
    for i in range(0, 9):
        p_ls.append(df.loc[df['study_level'] == 'P{}'.format(str(i))])
    p_ls.append(df.loc[df['study_level'] == "PP"])
    for i in p_ls:
        try:
            pp_ls.append(len(i.index))
        except:
            pp_ls.append(0)
    return pp_ls
