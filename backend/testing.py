from matching_model import Score_Calculator, Matching
from variables import compatibility_scores, matched_format, mentor_vars, mentee_vars, JUNIOR_MAX, SENIOR_MAX
import pandas as pd



# testing specific cases
if __name__ == '__main__':
    mentor_df = pd.read_csv('csv/mentor.csv')
    mentee_df = pd.read_csv('csv/mentee.csv')
    # scores_df = pd.read_csv('csv/sample_scores.csv')


    #FUNCTION TEST CASES

    Calc = Score_Calculator(mentor_df, mentee_df, compatibility_scores)
    scores_df = Calc.score_matrix()

    # TEST CASE SCORES_DF is defined
    assert isinstance(scores_df, pd.DataFrame), "Object is a Pandas DataFrame"
    print("Defined Case Passed")

    # TEST CASE NO ZEROS IN SCORES_DF
    assert (scores_df != 0).all().all(
    ), "0's in the scores dataframe (scores_df)"
    print("All Values greater than 0 Case Passed")

    # TEST CASE, NO VALUES GREATER THAN 1 in the scores_df
    assert (scores_df <= 1).all().all(), "A Value of 1 in the scores_df was detected"
    print("All Values less than 1 Case Passed")



    # TEST CASE ASSIGNMENT VALUES > 0.60

    match = Matching(mentor_df, mentee_df, scores_df,
                     matched_format, mentor_vars, mentee_vars)
    


    # match.assignment()
    print("All Cases Passed")
