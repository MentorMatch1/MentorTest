import json
import pandas as pd
from matching_model import Score_Calculator, Matching
from cohort_model import cohortModel, assignCohort
from variables import (
    compatibility_scores,
    matched_format,
    mentor_vars,
    mentee_vars,
    cohorts,
)
from config_manager import update_config


# data: dictionary of json {'mentee': json, mentor: 'json'}
def match_mentor_mentee(data: json):
    mentee_df = pd.read_json(data["mentee"], orient="records")
    mentor_df = pd.read_json(data["mentor"], orient="records")

    if mentee_df is None or mentor_df is None:
        raise Exception(
            "The mentor data or mentee data was not succesfully recieved",
        )

    score_calculator = Score_Calculator(mentor_df, mentee_df, compatibility_scores)
    scores_df = score_calculator.score_matrix()
    matching_instance = Matching(
        mentor_df, mentee_df, scores_df, matched_format, mentor_vars, mentee_vars
    )

    matched_df = matching_instance.assignment()
    mentor_assigned_info = matching_instance.mentor_matches()

    # using json.dumps(matched_df) to change the dictionary into a json string to prevent the order of dictionary keys/values to be changed
    response_data = {
        "message": "Data Recieved Sucessfully",
        "matches": json.dumps(matched_df),
        "info": json.dumps(mentor_assigned_info),
    }
    return response_data


def match_cohort(data: dict):
    mentee_df = pd.read_json(data["mentee"], orient="records")

    if mentee_df is None:
        raise Exception("Mentor Data or Mentee Data was not successfully recieved")

    cohort_model_instance = cohortModel(cohorts, mentee_df)
    compatibility_scores_cohort = cohort_model_instance.cohortScores()

    reccomended_cohorts = assignCohort(compatibility_scores_cohort)
    response_data = {"reccomended": json.dumps(reccomended_cohorts)}

    return response_data


def update_max_junior(max_junior: int):
    assert max_junior > 0, "Max junior must be more than 0"
    update_config("JUNIOR_MAX", max_junior)
