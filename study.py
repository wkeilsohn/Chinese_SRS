# William Keilsohn
# September 26 2025

###
# This file essentially acts as the "Brain" of the SRS Program.
###

# Import Packages
import numpy as np
import pandas as pd
from time_manager import *
import math
from cmd_interface import *
from hanzi_loader import get_user_words

# Declare Variables
hanzi_df = pd.DataFrame() # This is temporart

# Define Functions
def get_first_words(hanzi_df):
    return hanzi_df.head(5)

def get_current_hanzi_sheet(user_df):
    current_sheet = user_df.tail(1)["Sheet_Level"]
    hanzi_df_path = os.path.join(hpath, "HV{}.csv".format(current_sheet))
    return get_user_words(num_file=hanzi_df_path)

# def get_next_sheet(hanzi_df, last_word):
#     if hanzi_df.tail(1)["Word"] == last_word:


def get_next_set(hanzi_df, last_word):
    current_loc = hanzi_df[hanzi_df["Word"] == last_word].index[0]
    start_loc = current_loc + 1
    end_loc =  start_loc + 5
    return hanzi_df.iloc[start_loc:end_loc]

def build_user_data(username, starting_words, word_level=1):
    tmp_df = starting_words
    tmp_df["User_Name"] = username
    tmp_df["Last_Studied"] = datetime.now()
    tmp_df["Study_Level"] = "PP"
    tmp_df["Word_Level"] = word_level
    tmp_df["Inccorect_Times"] = 0
    return tmp_df

def check_word_level(user_df):
    current_level = user_df.tail(1)["Word_Level"]
    new_level = current_level + 1
    return new_level

def add_new_user_words(hanzi_df, user_df):
    user_info = user_df.tail(1)
    user_name = user_info["User_Name"][0]
    last_word = user_info["Word"][0]
    new_words = get_next_set(hanzi_df=hanzi_df, last_word=last_word)
    new_word_level = check_word_level(user_df=user_df)
    user_words = build_user_data(username=user_name, starting_words=new_words, word_level=new_word_level)
    total_words = pd.concat([user_df, user_words], ignore_index=True)
    return total_words
    
def update_SRS_level(inc_times, study_level, inc_value): # Return the new SRS Level
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
    if level_change < 0: # I wish I had 0 wishes
        level_change = 0 # Granted. You now have 255 wishes.
    new_level = list(time_dict.keys())[level_change]
    # print(new_level)
    return new_level

def study_word(user_word_input, word_def_val):
    if word_def_val != user_word_input:
        return 1
    else:
        return 0

def check_if_need_to_study(user_df):
    global format_string
    word_ls = list(user_df["Meaning"])
    for index, row in user_df.iterrows():
        try:
            last_study_date = datetime.strptime(row["Last_Studied"], format_string)
        except:
            last_study_date = datetime.now() # Error only occurs when crearing new user. 
        time_since_studied = calculate_time_since_last_study(last_review_time=last_study_date)
        study_needed = check_if_study(p_val=row["Study_Level"], review_time=time_since_studied)
        if not study_needed:
            pass
        else:
            answer_ls = create_answer_ls(word_ls=word_ls, answer=row["Meaning"]) # May keep this.
            user_value = interface_study_word(row, answer_ls) # Needs to be updated to a web gui latter. 
            user_df.at[index, "Last_Studied"] = datetime.now()
            study_result = study_word(user_value, row["Meaning"])
            inc_val = row["Inccorect_Times"] + study_result
            user_df.at[index, "Inccorect_Times"] = inc_val
            user_df.at[index, "Study_Level"] = update_SRS_level(inc_times=inc_val, study_level=row["Study_Level"], inc_value=study_result)
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
    if len(passed_words) >= math.ceil(3 *(len(user_progress) / 4)):
        return True
    else:
        return False
    
def user_advance(hanzi_df, user_df):
    user_status = check_for_user_progress(user_df=user_df)
    if user_status == True:
        add_new_user_words(hanzi_df=hanzi_df, user_df=user_df)
        check_if_need_to_study(user_df=user_df) # Forces the user to study the new words. 