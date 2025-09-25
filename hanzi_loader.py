# William Keilsohn
# September 11 2025

# Import Packages
import os
import pandas as pd

# Define variables
cpath = os.getcwd()
hpath = os.path.join(cpath, "Hanzi")

HSK_1_file = os.path.join(hpath, "HV1.csv")
HSK_2_file = os.path.join(hpath, "HV2.csv")
HSK_3_file = os.path.join(hpath, "HV3.csv")
HSK_4_file = os.path.join(hpath, "HV4.csv")
HSK_5_file = os.path.join(hpath, "HV5.csv")
HSK_6_file = os.path.join(hpath, "HV6.csv")

# Define Functions

def load_vocab(file_path):
    vocab = pd.read_csv(file_path, header=0)
    return vocab

def vocab_cleaner(vdf, ct_val):
    if ct_val <= 0:
        df = vdf[['Word', 'Meaning']]
    else:
        df = vdf[['Traditional_Word', 'Meaning']]
    return df
