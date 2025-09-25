# William Keilsohn
# September 25 2025

####
# This file is meant to simulate the role / interaction of a database until one can be obtained.
####

# Import Packages
import os
import pandas as pd
from hanzi_loader import *

# Define Global Variables

user_words = pd.DataFrame()

# Define Functions

# Run Application
if __name__=="__main__":
    raw_vdf = load_vocab(HSK_1_file)
    clean_df = vocab_cleaner(raw_vdf, 0)
    print(clean_df)