import ollama
import pandas as pd
import numpy as np
from variables import cohorts
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import copy

#1

class cohortModel:
    def __init__(self, cohorts, mentee_df):
        '''
        cohorts = dict keys=strings values=strings
        mentee_df = dataframe object
        mentee_id_list = list, index=int
        
        '''
        self.cohorts = cohorts
        self.mentee_df = mentee_df
        self.mentee_id_list = list(self.mentee_df['Mentee ID'])
        

    def embed_descriptions(self, descriptions):
        '''embed both the mentee requests and the cohort descriptions created, returns a multi dimensional array 
        rows = list of embeddings
        columns = embedding list of each word
        '''
        for i in range(len(descriptions)):
            descriptions[i] = ollama.embeddings(model='mxbai-embed-large', prompt=descriptions[i])['embedding']
        return np.array(descriptions)
    

    def create_compatibility_matrix(self):
        self.compatibility_matrix = pd.DataFrame(columns=list(cohorts.keys()), index=self.mentee_id_list)
        self.compatibility_matrix = self.compatibility_matrix.fillna(0)
        self.compatibility_matrix = self.compatibility_matrix.astype(float)

    # def compare_cohorts_requests_2(self):

    #     embedding_weight = 0.9
    #     tfidf_weight = 0.1
        
    #     embed_cohort_descriptions = self.embed_descriptions(list(cohorts.values()))
    #     embed_mentee_requests = self.embed_descriptions(list(self.mentee_df['Mentee Requests']))

    #     combined_texts = list(cohorts.values()) + list(self.mentee_df['Mentee Requests'])

    #     tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    #     tfidf_matrix = tfidf_vectorizer.fit_transform(combined_texts).toarray()

    #     tf_idf_descriptions = tfidf_matrix[:len(cohorts)].copy()
    #     tf_idf_requests = tfidf_matrix[len(cohorts):].copy()

    #     normalized_cohort_embeddings = normalize(embed_cohort_descriptions, norm='l2')
    #     normalized_request_embeddings = normalize(embed_mentee_requests, norm='l2')

    #     combined_cohort = np.hstack((normalized_cohort_embeddings * embedding_weight, tf_idf_descriptions * tfidf_weight))
    #     combined_requests = np.hstack((normalized_request_embeddings * embedding_weight, tf_idf_requests * tfidf_weight))

    #     similarity_matrix = cosine_similarity(combined_cohort, combined_requests)
    #     print(similarity_matrix)

    def compare_cohorts_requests(self):

        embed_cohort_descriptions = self.embed_descriptions(list(cohorts.values()))
        embed_mentee_requests = self.embed_descriptions(list(self.mentee_df['Mentee Requests']))

        normalized_cohort_embeddings = normalize(embed_cohort_descriptions, norm='l2')
        normalized_request_embeddings = normalize(embed_mentee_requests, norm='l2')


        similarity_matrix = cosine_similarity(normalized_request_embeddings, normalized_cohort_embeddings)
        print(similarity_matrix)

       
        for i,mentee_id in enumerate(self.mentee_id_list):
            for j,cohort in enumerate(cohorts.keys()):
                self.compatibility_matrix.loc[mentee_id,cohort] += similarity_matrix[i][j]

        print(self.compatibility_matrix)

    def cohortScores(self):

        self.create_compatibility_matrix()
        self.compare_cohorts_requests()

        return self.compatibility_matrix




class assignCohort:
    def __init__(self, cohortScores, mentee_df):
        pass
        

if __name__ == '__main__':
    mentee_df = pd.read_csv('csv/mentee_2.csv')
    cohort_test = cohortModel(cohorts, mentee_df)
    cohort_test.cohortScores()


