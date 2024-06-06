from quart import Quart, jsonify, request, abort
# from quart_cors import cors
# from quart_auth import AuthManager, login_user, logut_user, current_user, login_required, User

import json
import pandas as pd
from model import matching_scores

# export QUART_APP=api:app
# quart run
# source mentor_env/bin/activate
app = Quart(__name__)


@app.post("/csv")
async def csv_intake():
    # dictionary of json {'mentee': json, mentor: 'json'}
    data = await request.get_json()
    print(type(data['mentee']))
    mentee_df = pd.read_json(data['mentee'], orient='records')
    mentor_df = pd.read_json(data['mentor'], orient='records')

    if mentee_df is None or mentor_df is None:
        abort(
            400, description="The mentor data or mentee data was not succesfully recieved")

    scores_df_json = matching_scores(mentee_df, mentor_df)

    response_data = {'message': 'Data Recieved Sucessfully',
                     'scores': scores_df_json}
    return jsonify(response_data), 200

if __name__ == '__main__':
    # current port 5001
    app.run(host='0.0.0.0', port=5001)
