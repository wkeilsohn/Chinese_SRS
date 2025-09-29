# William Keilsohn
# September 29 2025

###
# This file is just to access the SRS from the command line. A Web GUI should be built out later. 
###

# Import Packages
from random import randint
import pandas as pd

# Define Functions

def create_answer_ls(word_ls, answer):
    indxs = [randint(0, len(word_ls)) for x in range (3)]
    indxs = [x - 1 if x >= len(word_ls) else x for x in indxs]
    ans = [word_ls[x] for x in indxs]
    y = randint(0, len(ans))
    ans.insert(y, answer)
    return ans

def create_answer_options(answer_ls):
    answer_df = pd.DataFrame(answer_ls)
    return answer_df

def interface_study_word(word_ls, answer_ls):
    answer_df = answer_df = create_answer_options(answer_ls)
    print("What does this character mean? \n")
    print(word_ls["Word"])
    print("\n")
    print(answer_df, "\n")
    user_answer = int(input("Please select the number that goes with the answer: "))
    answer_given = answer_df.loc[user_answer, 0]
    return answer_given