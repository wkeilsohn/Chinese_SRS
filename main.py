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

# Run Application
if __name__=="__main__":
    raw_vdf = load_vocab(HSK_1_file)
    clean_df = vocab_cleaner(raw_vdf, 0)
    user_name = get_user_name()
    starting_words = get_first_words(hanzi_df=clean_df)
    user_df = build_user_data(username=user_name, starting_words=starting_words)
    print(user_df)
