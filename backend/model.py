from variables import compatibility_scores, matched_format,mentor_vars,mentee_vars
import ollama
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

pd.set_option('future.no_silent_downcasting', True)


def create_scores_df(mentee_id_list, mentor_id_list):
    '''creating a dataframe matrix of scores

    rows: mentors
    columns: mentees

    return: scores dataframe with 0's inside of the matrix

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

            mentor_column = dict(mentor_df.loc[mentor_id])['Mentor Residence']
            mentee_column = dict(mentee_df.loc[mentee_id])['Mentee Residence']

            if (mentor_column == mentee_column):
                scores_df.loc[mentor_id, mentee_id] += round(weighting, 2)

def assignment(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list):
    '''takes the score matrix and returns a csv file that gives all the matches with their names
    scores_matrix_df -> rows = mentor ids / columns = mentee ids
    scores_matrix_df.loc[mentor_id, mentee_id] = int

    cols (mentees) iterated then mentors as we have to give each mentee a pairing.
    '''
    
    mentor_assigned_count = {key: [] for key in mentor_id_list}

    for mentee_id in mentee_id_list:

        largest_match_score = 0
        index = 0

        for i,mentor_id in enumerate(mentor_id_list): 
            if scores_matrix_df.loc[mentor_id, mentee_id] > largest_match_score:
                index = i
                largest_match_score = scores_matrix_df.loc[mentor_id, mentee_id]

        #Here, highest matching pair obtained, so add them to the dataframe from the scores obtained

        matched_format['Mentee ID'].append(mentee_id)
        for var in mentee_vars[1:]:
            matched_format[var].append(mentee_df.loc[mentee_id][var])

        matched_format['Mentor ID'].append(mentor_id_list[index])
        for var in mentor_vars[1:]:
            print(var)
            matched_format[var].append(mentor_df.loc[mentor_id_list[index]][var])


        matched_format['Score'].append(largest_match_score)
        mentor_assigned_count[mentor_id_list[index]].append(mentee_id)
        

    #print(matched_format)

    #test case
    #print(mentor_assigned_count)
    for key, value in matched_format.items():
        print(f"Length of list '{key}': {len(value)}")
    
    matched_df = pd.DataFrame(matched_format)
    matched_df.to_csv('output.csv', index=False)


def matching_scores(mentee_df, mentor_df):

    # retrieve all of the mentors and mentees in seperate lists
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
    
    print(scores_matrix_df)
    assignment(scores_matrix_df, mentee_df, mentor_df, mentee_id_list, mentor_id_list)

    return scores_matrix_df.to_json()


#Things to do
#Create better mentor/mentee files
#Add a max assignment limit for junior and senior mentees
#Create script to return CSV of the summary of all Mentors and Mentees matched with how many Mentees for the Mentor
#Fix Code, More Abstracting (Possibly make Mentors Columns and Mentees Rows?)



if __name__ == '__main__':
    mentor_df = pd.read_csv('../csv/mentor.csv')
    mentee_df = pd.read_csv('../csv/mentee.csv')
    matching_scores(mentee_df, mentor_df)

