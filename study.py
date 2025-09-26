# William Keilsohn
# September 26 2025

# Import Packages
import numpy as np
import pandas as pd
from time_manager import *

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
    return tmp_df
    
