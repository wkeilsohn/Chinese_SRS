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
### In prod, a DB will have a table for each user. Here, we will have one "table" (sheet) just for the admin account.


# Define Functions
def user_hanzi_reader(username): # Temp File Path
    return pd.read_csv(username)

def update_hanzi(hanzi_df): # Temp File Path
    global db_file_path
    try:
        hanzi_df.to_csv(db_file_path, index=False)
    except Exception as e:
        print(e)

### When a DB is used, SQLAlchemy will be needed to connect to the DB. 