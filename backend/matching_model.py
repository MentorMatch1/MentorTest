from variables import compatibility_scores, matched_format, mentor_vars, mentee_vars, JUNIOR_MAX
import ollama
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


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
        self.scores_df = pd.DataFrame(
            columns=self.mentee_id_list, index=self.mentor_id_list)
        self.scores_df = self.scores_df.fillna(0)

        self.scores_df = self.scores_df.astype(float)

    def embed_interests(self, interests):
        for i in range(len(interests)):
            interests[i] = ollama.embeddings(
                model='mxbai-embed-large', prompt=interests[i])['embedding']
        return np.array(interests)

    def compare_programs(self):
        for mentor_id in self.mentor_id_list:
            for mentee_id in self.mentee_id_list:
                mentor_program = self.mentor_df.loc[mentor_id,
                                                    'Mentor Program']
                mentee_program = self.mentee_df.loc[mentee_id,
                                                    'Mentee Program']

                self.scores_df.loc[mentor_id, mentee_id] = round(
                    (self.compatibility_scores[mentor_program][mentee_program] * 0.4) + self.scores_df.loc[mentor_id, mentee_id], 5)

    def compare_interests(self):
        embedded_mentor = self.embed_interests(
            list(self.mentor_df['Mentor Interests']))
        embedded_mentee = self.embed_interests(
            list(self.mentee_df['Mentee Interests']))

        similarity_matrix = cosine_similarity(embedded_mentor, embedded_mentee)
        print(similarity_matrix)

        for i, mentor_id in enumerate(self.mentor_id_list):
            for j, mentee_id in enumerate(self.mentee_id_list):
                self.scores_df.loc[mentor_id, mentee_id] = round(
                    (similarity_matrix[i][j] * 0.4) + self.scores_df.loc[mentor_id, mentee_id], 5)

    def compare_hobbies(self):
        ''' mentee_df[hobbies] and mentor_df[hobbies]

        embedding text
        cosine similarity
        
        '''
        pass

    def compare_residence(self):
        for mentor_id in self.mentor_id_list:
            for mentee_id in self.mentee_id_list:
                mentor_column = self.mentor_df.loc[mentor_id,
                                                   'Mentor Residence']
                mentee_column = self.mentee_df.loc[mentee_id,
                                                   'Mentee Residence']
                if mentor_column == mentee_column:
                    self.scores_df.loc[mentor_id, mentee_id] += round(0.2, 2)

    def score_matrix(self):
        '''parameter functions used to calculate the scores, returns the matrix of scores of mentord and mentees'''

        self.create_scores_df()
        self.compare_programs()
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
        self.matched_format = matched_format
        self.mentor_vars = mentor_vars
        self.mentee_vars = mentee_vars

        # New
        self.mentor_assigned_count = {key: [] for key in self.mentor_id_list}

    def assignment(self):
        for percentage in range(90, 50, -10):
            for mentee_id in list(self.mentee_id_list):
                score = 0
                largest_match_score = 0
                index = -1

                for i, mentor_id in enumerate(self.mentor_id_list):
                    score = self.scores_df.loc[mentor_id, mentee_id]

                    if score > largest_match_score:

                        if self.mentor_df.loc[mentor_id]['Mentor Role'] == 'Junior Science Mentor' and len(self.mentor_assigned_count[mentor_id]) < JUNIOR_MAX and mentee_id not in self.mentor_assigned_count[mentor_id] and score >= percentage / 100:
                            index = i
                            largest_match_score = score

                        if (len(self.mentor_assigned_count[mentor_id]) == JUNIOR_MAX and self.mentor_df.loc[mentor_id]['Mentor Role'] == 'Junior Science Mentor' and score > percentage / 100):
                            print(
                                f"Individuals Mentor ID: {mentor_id} with Mentee ID: {mentee_id} Could not be matched as there is a full amount of mentors assigned for mentor_id={mentor_id} {round(score, 5)}")

                if index > -1:
                    self.mentee_id_list.remove(mentee_id)
                    matched_format['Mentee ID'].append(mentee_id)
                    for var in self.mentee_vars[1:]:
                        matched_format[var].append(
                            self.mentee_df.loc[mentee_id][var])

                    matched_format['Mentor ID'].append(
                        self.mentor_id_list[index])
                    for var in mentor_vars[1:]:
                        matched_format[var].append(
                            self.mentor_df.loc[self.mentor_id_list[index]][var])

                    matched_format['Score'].append(
                        round(largest_match_score, 5))
                    self.mentor_assigned_count[self.mentor_id_list[index]].append(
                        mentee_id)
                    print(
                        f"Final Match - Mentee ID: {mentee_id} with Mentor ID: {self.mentor_id_list[index]}")
                    print('------------------------------------------------')

                elif index == -1 and largest_match_score < 0.60:
                    print(
                        f"{mentee_id} Could not be matched as their score was less than 0.60 after iterations OR mentor count was full")
                    print('---------------------------')

        print(self.mentor_assigned_count)
        print(self.mentee_id_list)

        self.matched_df = pd.DataFrame(matched_format)
        self.matched_df.to_csv('output.csv', orient='records')

       
        return self.matched_df.to_json(orient='records')

    def non_matched(self):
        '''returns all of the individuals who were not matched formatted into csv file'''
        return self.mentee_id_list


if __name__ == '__main__':

    mentor_df = pd.read_csv('csv/mentor.csv')
    mentee_df = pd.read_csv('csv/mentee.csv')

    Calc = Score_Calculator(mentor_df, mentee_df, compatibility_scores)
    scores_df = Calc.score_matrix()
    print(scores_df)

    match = Matching(mentor_df, mentee_df, scores_df,
                     matched_format, mentor_vars, mentee_vars)
    match.assignment()
