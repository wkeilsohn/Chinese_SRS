# William Keilsohn
# September 29 2025

###
# This file is just to access the SRS from the command line. A Web GUI should be built out later. 
###

# Import Packages
from random import randint

# Define Functions

def create_answer_ls(word_ls, answer):
    indxs = [randint(0, len(word_ls)) for x in range (3)]
    ans = [word_ls[x] for x in indxs]
    y = randint(0, 2)
    return ans.insert(y, answer)

def interface_study_word(word_ls, answer_ls):
    print("What does this character mean? \n")
    print(word_ls["Word"])
    print("\n")
    print(answer_ls, "\n")
    user_answer = input("Please select the number that goes with the answer: ")
    return answer_ls[user_answer]