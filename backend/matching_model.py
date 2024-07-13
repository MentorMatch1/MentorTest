from variables import compatibility_scores, matched_format, mentor_vars, mentee_vars, JUNIOR_MAX, mentors_matched_data
import ollama
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import copy

pd.set_option('future.no_silent_downcasting', True)

class Score_Calculator:
    '''creates all of the scores using the parameters here, returns the scores_dataframe to be used as needed'''

    def __init__(self, mentor_df, mentee_df, compatibility_scores):
        self.mentor_df = mentor_df.copy()
        self.mentee_df = mentee_df.copy()
        self.compatibility_scores = compatibility_scores

        self.mentor_id_list = list(self.mentor_df['Mentor ID'])
        self.mentee_id_list = list(self.mentee_df['Mentee ID'])

        self.mentor_df.set_index('Mentor ID', inplace=True)
        self.mentee_df.set_index('Mentee ID', inplace=True)

    def create_scores_df(self):
        self.scores_df = pd.DataFrame(columns=self.mentee_id_list, index=self.mentor_id_list)
        self.scores_df = self.scores_df.fillna(0)
        self.scores_df = self.scores_df.astype(float)

    def embed_interests(self, interests):
        for i in range(len(interests)):
            interests[i] = ollama.embeddings(model='mxbai-embed-large', prompt=interests[i])['embedding']
        return np.array(interests)

    def compare_programs(self):
        for mentor_id in self.mentor_id_list:
            for mentee_id in self.mentee_id_list:
                mentor_program = self.mentor_df.loc[mentor_id,'Mentor Program']
                mentee_program = self.mentee_df.loc[mentee_id,'Mentee Program']

                self.scores_df.loc[mentor_id, mentee_id] = round(
                    (self.compatibility_scores[mentor_program][mentee_program] * 0.35) + self.scores_df.loc[mentor_id, mentee_id], 5)

    def compare_interests(self):
        embedded_mentor = self.embed_interests(list(self.mentor_df['Mentor Interests']))
        embedded_mentee = self.embed_interests(list(self.mentee_df['Mentee Interests']))

        similarity_matrix = cosine_similarity(embedded_mentor, embedded_mentee)
        #print(similarity_matrix)

        for i, mentor_id in enumerate(self.mentor_id_list):
            for j, mentee_id in enumerate(self.mentee_id_list):
                self.scores_df.loc[mentor_id, mentee_id] = round(
                    (similarity_matrix[i][j] * 0.3) + self.scores_df.loc[mentor_id, mentee_id], 5)

    def compare_hobbies(self):
        ''' mentee_df[hobbies] and mentor_df[hobbies]
        embedding text
        cosine similarity
        '''
        
        embedded_mentor = self.embed_interests(list(self.mentor_df['Mentor Hobbies']))
        embedded_mentee = self.embed_interests(list(self.mentee_df['Mentee Hobbies']))

        similarity_matrix = cosine_similarity(embedded_mentor, embedded_mentee)
        #print(similarity_matrix)

        for i,mentor_id in enumerate(self.mentor_id_list):
            for j,mentee_id in enumerate(self.mentee_id_list):
               self.scores_df.loc[mentor_id,mentee_id] = round(similarity_matrix[i][j] * 0.25 + self.scores_df.loc[mentor_id, mentee_id], 5)
        

    def compare_residence(self):
        for mentor_id in self.mentor_id_list:
            for mentee_id in self.mentee_id_list:
                mentor_column = self.mentor_df.loc[mentor_id,
                                                   'Mentor Residence']
                mentee_column = self.mentee_df.loc[mentee_id,
                                                   'Mentee Residence']
                if mentor_column == mentee_column:
                    self.scores_df.loc[mentor_id, mentee_id] += round(0.1, 1)

    


    def score_matrix(self):
        '''parameter functions used to calculate the scores, returns the matrix of scores of mentors and mentees
        score key:
        1. Program of Study 35%
        2. Program Interests 30%
        3. Hobbies 25%
        4. Residence 10%
        '''

        self.create_scores_df()
        self.compare_programs()
        self.compare_hobbies()
        self.compare_interests()
        self.compare_residence()

        return self.scores_df


class Matching:
    '''Physical matching of all the scores given requires 6 arguments
    1. mentor dataframe  2. mentee dataframe
    3. scores matrix from Score_Calculator class 4. matched_format (from variables) 5. mentor_vars (from variables) 6. mentee_vars (from variables)

    returns: matched_format that contains all of the data of matches ready to be processed into a csv file

    '''

    def __init__(self, mentor_df, mentee_df, scores_df, matched_format, mentor_vars, mentee_vars):
        self.mentor_df = mentor_df.copy()
        self.mentee_df = mentee_df.copy()

        self.mentor_id_list = list(self.mentor_df['Mentor ID'])
        self.mentee_id_list = list(self.mentee_df['Mentee ID'])

        self.mentor_df.set_index('Mentor ID', inplace=True)
        self.mentee_df.set_index('Mentee ID', inplace=True)

        self.scores_df = scores_df
        self.matched_format = copy.deepcopy(matched_format)
        self.mentor_vars = copy.deepcopy(mentor_vars)
        self.mentee_vars = copy.deepcopy(mentee_vars)

        # New
        self.mentor_assigned_count = {key: [] for key in self.mentor_id_list}
        self.mentor_assigned_data = copy.deepcopy(mentors_matched_data)

    def assign_mentor_mentee(self, mentee_id, index, largest_match_score):
        '''assigns the highest score avaliable mentor to the mentee selected'''

        self.mentee_id_list.remove(mentee_id)
        self.matched_format['Mentee ID'].append(mentee_id)

        for var in self.mentee_vars[1:]:
            self.matched_format[var].append(self.mentee_df.loc[mentee_id][var])

        self.matched_format['Mentor ID'].append(self.mentor_id_list[index])
        for var in mentor_vars[1:]:
            self.matched_format[var].append(self.mentor_df.loc[self.mentor_id_list[index]][var])

        self.matched_format['Score'].append(round(largest_match_score, 5))
        self.mentor_assigned_count[self.mentor_id_list[index]].append(mentee_id)

    def assignment(self) -> dict:
        for percentage in range(90, 50, -10):
            print(f'iteration ------------ {percentage}')
            for mentee_id in list(self.mentee_id_list):
                score = 0
                largest_match_score = 0
                best_mentor_index = -1

                for i, mentor_id in enumerate(self.mentor_id_list):
                    score = self.scores_df.loc[mentor_id, mentee_id]

                    if score > largest_match_score:

                        if self.mentor_df.loc[mentor_id]['Mentor Role'] == 'Junior Science Mentor' and len(self.mentor_assigned_count[mentor_id]) < JUNIOR_MAX and mentee_id not in self.mentor_assigned_count[mentor_id] and score >= percentage / 100:
                            best_mentor_index = i
                            largest_match_score = score

                        # if (len(self.mentor_assigned_count[mentor_id]) == JUNIOR_MAX and self.mentor_df.loc[mentor_id]['Mentor Role'] == 'Junior Science Mentor' and score > percentage / 100):
                        #     print(
                        #         f"Individuals Mentor ID: {mentor_id} with Mentee ID: {mentee_id} Could not be matched as there is a full amount of mentors assigned for mentor_id={mentor_id} {round(score, 5)}")

                if best_mentor_index > -1:
                    self.assign_mentor_mentee(mentee_id, best_mentor_index, largest_match_score)

                    print(f"Final Match - Mentee ID: {mentee_id} with Mentor ID: {self.mentor_id_list[best_mentor_index]} score: {largest_match_score}")
                    print('------------------------------------------------')

                elif best_mentor_index == -1 and largest_match_score < 0.60:
                    print(f"{mentee_id} Could not be matched as their score was less than 0.60 after iterations OR mentor count was full")
                    print('---------------------------')

        #print(self.mentor_assigned_count)
        #print(self.mentee_id_list)

        for i in range(len(self.matched_format['Mentor Residence'])):
            if(not isinstance(self.matched_format['Mentor Residence'][i], bool)):
                self.matched_format['Mentor Residence'][i] = bool(self.matched_format['Mentor Residence'][i])

        for i in range(len(self.matched_format['Mentee Residence'])):
            if(not isinstance(self.matched_format['Mentee Residence'][i], bool)):
                self.matched_format['Mentee Residence'][i] = bool(self.matched_format['Mentee Residence'][i])


        return self.matched_format

    def non_matched(self):
        '''returns all of the individuals who were not matched formatted into csv file'''
        return self.mentee_id_list
    
    
    def mentor_matches(self) -> dict:
        '''takes in all of the mentors that have their matches and lists their match and the amount of people their matched to'''
        mm_data_keys = list(self.mentor_assigned_data.keys())
        for key in self.mentor_assigned_count.keys():

            #iterates through all of the mentors_matched_data keys except for 'Mentor Assigned Count', 'Assigned to'
            self.mentor_assigned_data['Mentor ID'].append(key)
            for i in range(1,len(mm_data_keys) - 2):
                self.mentor_assigned_data[mm_data_keys[i]].append(self.mentor_df.loc[key][mm_data_keys[i]])
            
            self.mentor_assigned_data['Mentor Assigned Count'].append(len(self.mentor_assigned_count[key]))
            self.mentor_assigned_data['Mentees Assigned'].append(''.join( str(mentee) + ' ' for mentee in self.mentor_assigned_count[key]))


        return self.mentor_assigned_data
        




    
if __name__ == '__main__':

    mentor_df = pd.read_csv('csv/mentor.csv')
    mentee_df = pd.read_csv('csv/mentee.csv')

    Calc = Score_Calculator(mentor_df, mentee_df, compatibility_scores)
    scores_df = Calc.score_matrix()
    print(scores_df)

    match = Matching(mentor_df, mentee_df, scores_df,
                     matched_format, mentor_vars, mentee_vars)
    match.assignment()
