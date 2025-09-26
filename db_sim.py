# William Keilsohn
# September 25 2025

####
# This file is meant to simulate the role / interaction of a database until one can be obtained.
# ATM (09/25/2025) this is beeing done with a CSV file. Ideally this will be moved to a DB later. 
####

# Import Packages
import os
import pandas as pd
from hanzi_loader import *

# Define Global Variables
user_words = pd.DataFrame()
c_path = os.getcwd()
db_path = os.path.join(cpath, "DB_SIM")

db_file_path = os.path.join(db_path, "db_file.csv") #This is going to act like a DB ATM.

# Define Functions

# Run Application
if __name__=="__main__":
    raw_vdf = load_vocab(HSK_1_file)
    clean_df = vocab_cleaner(raw_vdf, 0)
    print(clean_df)