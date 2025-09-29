# William Keilsohn
# September 11 2025

# Import Packages
import numpy as np
import pandas as pd
import os
from datetime import datetime
import warnings

## Manage Warnings
warnings.simplefilter('ignore')

## Import Custom Scripts
from hanzi_loader import *
from time_manager import *
from user import *
from study import *

### Temp File (Replace in Prod)
from db_sim import *

# Define Global Variables

# Define Functions

### These functions may become obsolete very quickly

def create_first_words():
    raw_vdf = load_vocab(HSK_1_file)
    clean_df = vocab_cleaner(raw_vdf, 0)
    starting_words = get_first_words(hanzi_df=clean_df)
    return starting_words

def check_existing_users(user_name):
    try:
        user_data = pd.read_csv(db_file_path)
        user_df = user_data[user_data["User_Name"] == user_name]
    except:
        starting_words = create_first_words()
        user_df = build_user_data(username=user_name, starting_words=starting_words)
    return user_df

###

# Run Application
if __name__=="__main__":
    user_name = get_user_name()
    user_df = check_existing_users(user_name=user_name)
    user_df = check_if_need_to_study(user_df=user_df)
    update_hanzi(user_df)
