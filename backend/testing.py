from model import create_scores_df, compare_programs, embed_interests, compare_interests, compare_static, assignment
from variables import mentor_vars, mentee_vars
import pandas as pd


#testing specific cases

if __name__ == '__main__':
    mentor_df = pd.read_csv('csv/mentor.csv')
    mentee_df = pd.read_csv('csv/mentee.csv')
    scores_df = pd.read_csv('csv/sample_scores.csv')

    

    # ---------------------------------------------
    # CHANGES -------------------------------------
    # ---------------------------------------------

    mentee_id_list = list(mentee_df['Mentee ID'])
    mentor_id_list = list(mentor_df['Mentor ID'])

    # removing index
    mentor_df.set_index('Mentor ID', inplace=True)
    mentee_df.set_index('Mentee ID', inplace=True)

    scores_matrix_df = create_scores_df(mentee_id_list, mentor_id_list)

    # Comparing mentors to mentees to get all the scores
    compare_programs(scores_matrix_df, mentee_df, mentor_df,
                     mentee_id_list, mentor_id_list)
    compare_static(scores_matrix_df, mentee_df, mentor_df,
                   mentee_id_list, mentor_id_list, 'Residence', 0.2)
    
    compare_interests(scores_matrix_df, mentee_df, mentor_df,
                      mentee_id_list, mentor_id_list)

    #scores_matrix_df.to_csv('scores.csv', index=False)
    assignment(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list)
    
    
    
    
    




