# William Keilsohn
# September 11 2025

# Import Packages
import numpy as np
import pandas as pd
import os

## Import Custom Scripts
from hanzi_loader import *
from time_manager import *

### Temp File (Replace in Prod)
from db_sim import *

# Define Global Variables

# Define Functions

# Run Application
if __name__=="__main__":
    raw_vdf = load_vocab(HSK_1_file)
    clean_df = vocab_cleaner(raw_vdf, 0)
    print(clean_df)
