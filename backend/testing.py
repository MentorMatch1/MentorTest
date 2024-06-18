from model import create_scores_df, compare_programs, embed_interests, compare_interests, compare_static
from variables import mentor_vars, mentee_vars
import pandas as pd


#testing specific cases

if __name__ == '__main__':
    mentor_df = pd.read_csv('../csv/mentor.csv')
    mentee_df = pd.read_csv('../csv/mentee.csv')
    #print('Checking create_scores_df function')
    print(mentor_vars)




