import ollama
import pandas as pd
import numpy as np
from variables import cohorts
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize


class cohortModel:
    def __init__(self, cohorts, mentee_df):
        """
        cohorts = dict keys=strings values=strings
        mentee_df = dataframe object
        mentee_id_list = list, index=int

        """
        self.cohorts = cohorts
        self.mentee_df = mentee_df
        self.mentee_id_list = list(self.mentee_df["Mentee ID"])

    def embed_descriptions(self, descriptions):
        """embed both the mentee requests and the cohort descriptions created, returns a multi dimensional array
        rows = list of embeddings
        columns = embedding list of each word
        """
        for i in range(len(descriptions)):
            descriptions[i] = ollama.embeddings(
                model="mxbai-embed-large", prompt=descriptions[i]
            )["embedding"]
        return np.array(descriptions)

    def create_compatibility_matrix(self):
        self.compatibility_matrix = pd.DataFrame(
            columns=list(cohorts.keys()), index=self.mentee_id_list
        )
        self.compatibility_matrix = self.compatibility_matrix.fillna(0)
        self.compatibility_matrix = self.compatibility_matrix.astype(float)

    def compare_cohorts_requests(self):
        embed_cohort_descriptions = self.embed_descriptions(list(cohorts.values()))
        embed_mentee_requests = self.embed_descriptions(
            list(self.mentee_df["Mentee Requests"])
        )

        normalized_cohort_embeddings = normalize(embed_cohort_descriptions, norm="l2")
        normalized_request_embeddings = normalize(embed_mentee_requests, norm="l2")

        similarity_matrix = cosine_similarity(
            normalized_request_embeddings, normalized_cohort_embeddings
        )

        for i, mentee_id in enumerate(self.mentee_id_list):
            for j, cohort in enumerate(cohorts.keys()):
                self.compatibility_matrix.loc[mentee_id, cohort] += similarity_matrix[
                    i
                ][j]

    def cohortScores(self):
        self.create_compatibility_matrix()
        self.compare_cohorts_requests()

        return self.compatibility_matrix


class assignCohort:
    def __init__(self, cohortScores, mentee_df):
        self.cohortScores = cohortScores
        self.cohortMatchDict = {
            "mentee_ids": [],
            "firstnames": [],
            "lastnames": [],
            "programs": [],
            "assigned_to": [],
            "scores": [],
        }
        self.mentee_df = mentee_df

    def assignment(self):
        for index, row in self.cohortScores.iterrows():
            # Get the top three values and their corresponding columns
            top_three = row.nlargest(3)
            mentee_row = self.mentee_df[self.mentee_df["Mentee ID"] == index]
            first_name = mentee_row["Mentee Firstname"].values[0]
            last_name = mentee_row["Mentee Lastname"].values[0]
            program = mentee_row["Mentee Program"].values[0]
            assigned_to = list(top_three.index)
            assigned_to = ", ".join(assigned_to)
            scores = [round(float(score), 2) for score in top_three.values]
            # Store the top three column names in the dictionary
            self.cohortMatchDict["mentee_ids"].append(index)
            self.cohortMatchDict["firstnames"].append(first_name)
            self.cohortMatchDict["lastnames"].append(last_name)
            self.cohortMatchDict["programs"].append(program)
            self.cohortMatchDict["scores"].append(scores)
            self.cohortMatchDict["assigned_to"].append(assigned_to)

        return self.cohortMatchDict


def main():
    mentee_df = pd.read_csv("csv/mentee.csv")
    cohort_test = cohortModel(cohorts, mentee_df)

    cohort_scores = cohort_test.cohortScores()
    assignCohortInstance = assignCohort(cohort_scores, mentee_df)

    reccomend_cohort = assignCohortInstance.assignment()
    print(reccomend_cohort)
    cohort_assigned = pd.DataFrame(reccomend_cohort)
    cohort_assigned.to_csv("csv/cohortReccomended.csv", index=True)


if __name__ == "__main__":
    main()
