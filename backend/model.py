from variables import compatibility_scores
import ollama
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

pd.set_option('future.no_silent_downcasting', True)


def create_scores_df(mentee_id_list, mentor_id_list):
    '''creating a dataframe matrix of scores

    rows: mentors
    columns: mentees

    '''
    scores_df = pd.DataFrame(columns=mentee_id_list, index=mentor_id_list)
    scores_df = scores_df.fillna(0)

    # making sure that all values in the matrix are floats
    scores_df = scores_df.astype(float)

    return scores_df


def compare_programs(scores_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list):
    '''
    takes a mentor id, mentor_df.loc[mentor_id] grabs all of the data from that row from the mentor_df
    mentee_df.loc[mentee_id] grabs all of the data from that row from the mentee_df

    ['program'] is called on the dictionary to grab the program data for that specific id

    .loc selects a single row here

    '''
    for mentor_id in mentor_id_list:
        for mentee_id in mentee_id_list:

            mentor_program = dict(mentor_df.loc[mentor_id])['Mentor Program']
            mentee_program = dict(mentee_df.loc[mentee_id])['Mentee Program']

            scores_df.loc[mentor_id, mentee_id] = round(
                (compatibility_scores[mentor_program][mentee_program] * 0.4) + scores_df.loc[mentor_id, mentee_id], 5)


def embed_interests(interests):
    for i in range(len(interests)):
        interests[i] = ollama.embeddings(
            model='mxbai-embed-large', prompt=interests[i])['embedding']

    return np.array(interests)


def compare_interests(scores_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list):

    mentor_interests = list(mentor_df['Mentor Interests'])
    mentee_interests = list(mentee_df['Mentee Interests'])

    embedded_mentor = embed_interests(list(mentor_df['Mentor Interests']))
    embedded_mentee = embed_interests(list(mentee_df['Mentee Interests']))

    # the returned similarity matrix will have the first index 0 be the first row, and it rhe first index will contain all of the scores for all of the mentees
    # matched to that mentor in the row
    similarity_matrix = cosine_similarity(embedded_mentor, embedded_mentee)

    #print(similarity_matrix)

    for i, mentor_id in enumerate(mentor_id_list):
        for j, mentee_id in enumerate(mentee_id_list):
            scores_df.loc[mentor_id, mentee_id] = round(
                (similarity_matrix[i][j] * 0.4) + scores_df.loc[mentor_id, mentee_id], 5)


def compare_static(scores_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list, retrieve, weighting):
    '''for true or false comparisons (residence, international) similar implementation to the compare_programs function'''

    for mentor_id in mentor_id_list:
        for mentee_id in mentee_id_list:

            mentor_column = dict(mentor_df.loc[mentor_id])[retrieve]
            mentee_column = dict(mentee_df.loc[mentee_id])[retrieve]

            if (mentor_column == mentee_column):
                scores_df.loc[mentor_id, mentee_id] += round(weighting, 2)


def matching_scores(mentee_df, mentor_df):

    # retrieve all of the mentors and mentees in seperate lists
    mentee_id_list = list(mentee_df['id'])
    mentor_id_list = list(mentor_df['id'])

    # removing index
    mentor_df.set_index('id', inplace=True)
    mentee_df.set_index('id', inplace=True)

    scores_matrix_df = create_scores_df(mentee_id_list, mentor_id_list)

    # Comparing mentors to mentees to get all the scores
    compare_programs(scores_matrix_df, mentee_df, mentor_df,
                     mentee_id_list, mentor_id_list)
    compare_static(scores_matrix_df, mentee_df, mentor_df,
                   mentee_id_list, mentor_id_list, 'Residence', 0.2)
    
    compare_interests(scores_matrix_df, mentee_df, mentor_df,
                      mentee_id_list, mentor_id_list)
    
    print(scores_matrix_df)
    assignment(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list)

    return scores_matrix_df.to_json()

# assigning mentees to specific mentors


def assignment(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list):
    '''takes the score matrix and returns a csv file that gives all the matches with their names
    scores_matrix_df -> rows = mentor ids / columns = mentee ids
    scores_matrix_df.loc[mentor_id, mentee_id] = int


    
    '''

    matched_format = {
        'Mentee ID': [],
        'Mentee Firstname': [],
        'Mentee Lastname': [],
        'Mentee Email': [],
        'Mentee Program': [],
        'Mentee Interests': [],
        'Mentee Country': [],
        'Mentee City': [],
        'Mentee Residence': [],
        'Mentor ID': [],
        'Mentor Role': [],
        'Mentor Firstname': [],
        'Mentor Lastname': [],
        'Mentor Email': [],
        'Mentor Program': [],
        'Mentor Interests': [],
        'Mentor Country': [],
        'Mentor City': [],
        'Mentor Residence': [],
        'Score': []
    }

    for mentee_id in mentee_id_list:

        largest_match_score = 0
        index = 0

        for i,mentor_id in enumerate(mentor_id_list): 
            if scores_matrix_df.loc[mentor_id, mentee_id] > largest_match_score:
                index = i
                largest_match_score = scores_matrix_df.loc[mentor_id, mentee_id]

        #Here, highest matching pair obtained, so add them to the dataframe from the scores obtained

        matched_format['Mentee ID'].append(mentee_id)
        matched_format['Mentee Firstname'].append(mentee_df.loc[mentee_id]['Firstname'])
        matched_format['Mentee Lastname'].append(mentee_df.loc[mentee_id]['Lastname'])
        matched_format['Mentee Email'].append(mentee_df.loc[mentee_id]['Mentee Email'])
        matched_format['Mentee Program'].append(mentee_df.loc[mentee_id]['Mentee Program'])
        matched_format['Mentee Interests'].append(mentee_df.loc[mentee_id]['Mentee Interests'])
        matched_format['Mentee Country'].append(mentee_df.loc[mentee_id]['Mentee Country'])
        matched_format['Mentee City'].append(mentee_df.loc[mentee_id]['Mentee City'])
        matched_format['Mentee Residence'].append(mentee_df.loc[mentee_id]['Residence'])

        matched_format['Mentor ID'].append(mentor_id_list[index])
        matched_format['Mentor Role'].append(mentor_df.loc[mentor_id_list[index]]['Mentor Role'])
        matched_format['Mentor Firstname'].append(mentor_df.loc[mentor_id_list[index]]['Firstname'])
        matched_format['Mentor Lastname'].append(mentor_df.loc[mentor_id_list[index]]['Lastname'])
        matched_format['Mentor Email'].append(mentor_df.loc[mentor_id_list[index]]['Mentor Email'])
        matched_format['Mentor Program'].append(mentor_df.loc[mentor_id_list[index]]['Mentor Program'])
        matched_format['Mentor Interests'].append(mentor_df.loc[mentor_id_list[index]]['Mentor Interests'])
        matched_format['Mentor Country'].append(mentor_df.loc[mentor_id_list[index]]['Mentor Country'])
        matched_format['Mentor City'].append(mentor_df.loc[mentor_id_list[index]]['Mentor City'])
        matched_format['Mentor Residence'].append(mentor_df.loc[mentor_id_list[index]]['Residence'])
        matched_format['Score'].append(largest_match_score)
    

    matched_df = pd.DataFrame(matched_format)
    matched_df.to_csv('output.csv', index=False)
    


    print(scores_matrix_df.loc[312345,852367])

def mentor_assignment():
    '''gives the amount of mentees assigned to that specific mentor '''
    pass






if __name__ == '__main__':
    mentor_df = pd.read_csv('../csv/mentor.csv')
    mentee_df = pd.read_csv('../csv/mentee.csv')
    matching_scores(mentee_df, mentor_df)

