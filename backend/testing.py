from matching_model import Score_Calculator, Matching
from variables import compatibility_scores, matched_format, mentor_vars, mentee_vars, JUNIOR_MAX
import pandas as pd
from variables import JUNIOR_MAX



# testing specific cases
if __name__ == '__main__':
    mentor_df = pd.read_csv('csv/mentor_2.csv')
    mentee_df = pd.read_csv('csv/mentee_2.csv')
    # scores_df = pd.read_csv('csv/sample_scores.csv')


    #FUNCTION TEST CASES

    Calc = Score_Calculator(mentor_df, mentee_df, compatibility_scores)
    scores_df = Calc.score_matrix()

    # TEST CASE SCORES_DF is defined
    assert isinstance(scores_df, pd.DataFrame), "Object is a Pandas DataFrame"
    print("Defined Case Passed")

    # TEST CASE NO ZEROS IN SCORES_DF
    assert (scores_df != 0).all().all(), "0's in the scores dataframe (scores_df)"
    print("All Values greater than 0 Case Passed")

    # TEST CASE, NO VALUES GREATER THAN 1 in the scores_df
    assert (scores_df <= 1).all().all(), "A Value of 1 in the scores_df was detected"
    print("All Values less than 1 Case Passed")

    scores_df.to_csv('csv/scores.csv', index=True)

    # TEST CASE ASSIGNMENT VALUES > 0.60

    match = Matching(mentor_df, mentee_df, scores_df,
                     matched_format, mentor_vars, mentee_vars)

    
    matched_format = match.assignment()

    #Testing If The Return Type of the Matched_format after the assign function is a dictionary. 
    assert isinstance(matched_format, dict), "matched_format returned is not a dictionary"
    print("Matched_format is instance of dictionary test case passed")

    #Testing if all the Scores assigned by the Algorithm are above 0.60 atleast
    for score in matched_format['Score']:
        assert(score > 0.60), "One of the scores matched is less than 0.60, invalid match"
    print("Score above 0.60 case passed")

    #Testing if none of the mentors have more than 5
    for mentor_id in match.mentor_assigned_count.keys():
        assert(len(match.mentor_assigned_count[mentor_id]) <= JUNIOR_MAX), f"One of the mentors has more than JUNIOR_MAX={JUNIOR_MAX}"
    print(f"Mentors amount JUNIOR_MAX={JUNIOR_MAX} case passed")

    #Testing

    matched_format = pd.DataFrame(matched_format)
    matched_format.to_csv('csv/output.csv', index=True)


    mentor_matched_data = match.mentor_matches()
    mentor_matched_df = pd.DataFrame(mentor_matched_data)
    mentor_matched_df.to_csv('csv/mentor_matched_data.csv', index=True)

    

    # COHORT SCRIPT TESTING

    print("All Cases Passed")
