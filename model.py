import ollama
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

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
            
            scores_df.loc[mentor_id, mentee_id] = round((compatibility_scores[mentor_program][mentee_program] * 0.4) + scores_df.loc[mentor_id, mentee_id],2)

def embed_interests(interests):
    for i in range(len(interests)):
        interests[i] = ollama.embeddings(
            model='mxbai-embed-large', prompt=interests[i])['embedding']

    return np.array(interests)

def compare_interests(scores_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list):

    mentor_interests = list(mentor_df['interests'])
    mentee_interests = list(mentee_df['interests'])

    embedded_mentor = embed_interests(list(mentor_df['interests']))
    embedded_mentee = embed_interests(list(mentee_df['interests']))

    similarity_matrix = cosine_similarity(embedded_mentor, embedded_mentee)

    for index, mentor_id in enumerate(mentor_id_list):
        best_match_index = np.argmax(similarity_matrix[index])
        print(mentee_id_list[best_match_index])
        print(mentee_interests[best_match_index])
        print(mentor_id_list[index])
        print(mentor_interests[index])
        print(similarity_matrix[index][best_match_index])
        print('-------------------------------------')

        scores_df.loc[mentor_id, mentee_id_list[best_match_index]] = round((similarity_matrix[index][best_match_index] * 0.4) + scores_df.loc[mentor_id, mentee_id_list[best_match_index]],2)


def compare_static(scores_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list, retrieve, weighting):
    '''for true or false comparisons (residence, international)'''

    for mentor_id in mentor_id_list:
        for mentee_id in mentee_id_list:

            mentor_column = dict(mentor_df.loc[mentor_id])[retrieve]
            mentee_column = dict(mentee_df.loc[mentee_id])[retrieve]

            if(mentor_column == mentee_column):
                scores_df.loc[mentor_id, mentee_id] = round(scores_df.loc[mentor_id, mentee_id] + weighting,2)
                



    

def matching_scores():

    mentee_df = pd.read_csv('csv/mentee.csv')
    mentor_df = pd.read_csv('csv/mentor.csv')

    mentee_id_list = list(mentee_df['id'])
    mentor_id_list = list(mentor_df['id'])

    mentor_df.set_index('id', inplace=True)
    mentee_df.set_index('id', inplace=True)

    scores_matrix_df = create_scores_df(mentee_id_list, mentor_id_list)

    #Comparing mentors to mentees to get all the scores
    compare_programs(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list)
    #compare_static(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list, 'residence', 0.2)
    #compare_static(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list, 'international', 0.2)
    #compare_interests(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list)

    scores_matrix_df.to_csv('scores_df.csv')

# assigning mentees to specific mentors
def assign():
    pass




if __name__ == '__main__':
    matching_scores()



