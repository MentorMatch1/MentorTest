from quart import Quart, jsonify, request
#from quart_cors import cors
import json
import pandas as pd
from model import matching_scores

#export QUART_APP=api:app
#quart run
#source mentor_env/bin/activate
app = Quart(__name__)

@app.post("/csv")
async def csv_intake():
    data = await request.get_json() #dictionary of json {'mentee': json, mentor: 'json'} 
    print(type(data['mentee']))
    mentee_df = pd.read_json(data['mentee'],orient='records')
    mentor_df = pd.read_json(data['mentor'],orient='records')

    if mentee_df is None or mentor_df is None:
        abort(400, description="The mentor data or mentee data was not succesfully recieved")

    scores_df_json = matching_scores(mentee_df, mentor_df)

    response_data = {'message': 'Data Recieved Sucessfully', 'scores': scores_df_json}
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


    

