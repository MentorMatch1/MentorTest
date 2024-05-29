from quart import Quart, jsonify, request
#from quart_cors import cors
import json
import pandas as pd
from model import matching_scores

#export QUART_APP=api:app
#quart run
#source mentor_env/bin/activate
app = Quart(__name__)

# @app.route('/')
# async def index():
#     return 'hello'

@app.post("/csv")
async def csv_intake() -> str:
    data = await request.get_json() #dictionary of json {'mentee': json, mentor: 'json'} 
    mentee_df = data['mentee'].to_csv 
    mentor_df = data['mentor'].to_csv

    if mentee_df == None or mentor_df == None:
        abort(400, description="The mentor data or mentee data was not succesfully recieved")

    scores_df_json = matching_scores(mentee_df, mentor_df)

    response_data = {'message': 'Data Recieved Sucessfully', 'scores': scores_df_json}
    return response_data




    

