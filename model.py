import ollama
import numpy as np
import pandas as pd

def create_scores_df(mentee_df, mentor_df):
    #setting a scores matrix 
    scores_df = pd.DataFrame(columns=mentee_df)
