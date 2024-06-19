from model import create_scores_df, compare_programs, embed_interests, compare_interests, compare_static, assignment
from variables import mentor_vars, mentee_vars
import pandas as pd


#testing specific cases

if __name__ == '__main__':
    mentor_df = pd.read_csv('../csv/mentor.csv')
    mentee_df = pd.read_csv('../csv/mentee.csv')
    scores_df = pd.read_csv('../csv/sample_scores.csv')

    mentee_id_list = list(mentee_df['Mentee ID'])
    mentor_id_list = list(mentor_df['Mentor ID'])


    print('Checking create_scores_df function')
    print('-'*20)
    
    
    




