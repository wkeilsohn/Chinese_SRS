# William Keilsohn
# October 6th 2025

# Import Packages
import os
import django
import sys
import pandas as pd
from main.models import Hanzi
from SRS_Code.hanzi_loader import *

# Declare Valiables
sht_ls = [HSK_1_file, HSK_2_file, HSK_3_file, HSK_4_file, HSK_5_file, HSK_6_file]

# Declare functions
def sheet_loader():
    global sht_ls
    total_df = pd.DataFrame()
    for i in sht_ls:
        sht_df = load_vocab(i)
        total_df = pd.concat([total_df, sht_df], ignore_index=True)
    return total_df

def word_cleaner(df):
    df = df[["Word", "Traditional_Word", "Meaning", "Sheet_Level"]]
    return df

def upload_words(df):
    for index, row in df.iterrows():
        try:
            hanzi = Hanzi(word=row["Word"], traditional_word=row["Traditional_Word"], meaning=row["Meaning"], sheet_level=row["Sheet_Level"])
            hanzi.save()
        except Exception as e:
            print(e)

def full_upload():
    wdf = sheet_loader()
    wdf = word_cleaner(df=wdf)
    upload_words(df=wdf)

