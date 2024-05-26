import ollama
import numpy as np
import pandas as pd

pd.set_option('future.no_silent_downcasting', True)
from variables import compatibility_scores

def create_scores_df(mentee_id_list, mentor_id_list):
    scores_df = pd.DataFrame(columns=mentee_id_list, index=mentor_id_list)
    scores_df = scores_df.fillna(0)

    #making sure that all values in the matrix are floats
    scores_df = scores_df.astype(float)

    return scores_df

def compare_programs(scores_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list):
    for mentor_id in mentor_id_list:
        for mentee_id in mentee_id_list:

            mentor_program = dict(mentor_df.loc[mentor_id])['program']
            mentee_program = dict(mentee_df.loc[mentee_id])['program']
            
            scores_df.loc[mentor_id, mentee_id] = round(compatibility_scores[mentor_program][mentee_program] * 0.2,2)


def match():

    mentee_df = pd.read_csv('csv/mentee.csv')
    mentor_df = pd.read_csv('csv/mentor.csv')

    mentee_id_list = list(mentee_df['id'])
    mentor_id_list = list(mentor_df['id'])

    mentor_df.set_index('id', inplace=True)
    mentee_df.set_index('id', inplace=True)

    scores_matrix_df = create_scores_df(mentee_id_list, mentor_id_list)
    compare_programs(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list)

    scores_matrix_df.to_csv('scores_df.csv')


if __name__ == '__main__':
    match()



