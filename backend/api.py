from quart import Quart, jsonify, request, abort
import json

# from quart_cors import cors
# from quart_auth import AuthManager, login_user, logut_user, current_user, login_required, User

import pandas as pd
from matching_model import Score_Calculator, Matching
from variables import compatibility_scores, matched_format, mentor_vars, mentee_vars, JUNIOR_MAX

app = Quart(__name__)


@app.post("/csv")
async def csv_intake():
    # dictionary of json {'mentee': json, mentor: 'json'}
    data = await request.get_json()

    mentee_df = pd.read_json(data['mentee'], orient='records')
    mentor_df = pd.read_json(data['mentor'], orient='records')

    if mentee_df is None or mentor_df is None:
        abort(
            400, description="The mentor data or mentee data was not succesfully recieved")

    score_calculator = Score_Calculator(mentor_df,mentee_df,compatibility_scores)
    scores_df = score_calculator.score_matrix()
    matching_instance = Matching(mentor_df, mentee_df, scores_df, matched_format, mentor_vars, mentee_vars)
    matched_df = matching_instance.assignment()

    print(matched_df)

    #using json.dumps(matched_df) to change the dictionary into a json string to prevent the order of dictionary keys/values to be changed
    response_data = {'message': 'Data Recieved Sucessfully',
                     'matches': json.dumps(matched_df)}
    return jsonify(response_data), 200

if __name__ == '__main__':
    # current port 5001
    app.run(host='0.0.0.0', port=5001)
