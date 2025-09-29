# William Keilsohn
# September 26 2025

# Import Packages
import numpy as np
import pandas as pd
from time_manager import *
import math

# Define Global Variable

# Define Functions
def get_first_words(hanzi_df):
    return hanzi_df.head(5)

def get_next_set(hanzi_df, last_word):
    current_loc = hanzi_df[hanzi_df["Word"] == last_word].index[0]
    start_loc = current_loc + 1
    end_loc =  start_loc + 5
    return hanzi_df.iloc[start_loc:end_loc]

def build_user_data(username, starting_words):
    tmp_df = starting_words
    tmp_df["User_Name"] = username
    tmp_df["Last_Studied"] = 0
    tmp_df["Study_Level"] = "PP"
    tmp_df["Word_Level"] = 1
    tmp_df["Inccorect_Times"] = 0
    return tmp_df

def add_new_user_words(hanzi_df, user_df):
    user_info = user_df.tail(1)
    user_name = user_info["User_Name"][0]
    last_word = user_info["Word"][0]
    new_words = get_next_set(hanzi_df=hanzi_df, last_word=last_word)
    user_words = build_user_data(username=user_name, starting_words=new_words)
    total_words = pd.concat([user_df, user_words], ignore_index=True)
    return total_words
    
def update_SRS_level(inc_times, study_level): # Return the new SRS Level
    global time_dict
    inc_adjust = math.ceil(inc_times / 2)
    c_stage = list(time_dict()).index(study_level)
    c_adjust = 1
    if c_stage >= 5:
        c_adjust = 2
    level_change = math.floor(c_stage - (inc_adjust * c_adjust))
    return list(time_dict.keys())[level_change]

def study_word(user_word_input, word_def_val):
    if word_def_val != user_word_input:
        return 1
    else:
        return 0

def check_if_need_to_study(user_df):
    for index, row in user_df.iterrows():
        time_since_studied = calculate_time_since_last_study(last_review_time=row["Last_Studied"])
        study_needed = check_if_study(p_val=row["Study_Level"], review_time=time_since_studied)
        if not study_needed:
            pass
        else:
            user_value = interface_study_word() # Needs to be updated to a web gui latter. 
            row["Last_Studied"] = datetime.now()
            inc_val = row["Inccorect_Times"] + study_word(user_value, row["Meaning"])
            row["Inccorect_Times"] = inc_val
            row["Study_Level"] = update_SRS_level(inc_times=inc_val, study_level=row["Study_Level"])
    return user_df
