from quart import Quart, jsonify, request
#from quart_cors import cors
import json
import pandas as pd
from model import matching_scores

#export QUART_APP=api:app
#quart run

app = Quart(__name__)

# @app.route("/")
# async def index() -> str:
#     return 'hello'