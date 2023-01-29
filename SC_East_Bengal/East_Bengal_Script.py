#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch,Sbopen,VerticalPitch
import seaborn as sn

#Loading all the Football Competition Dataset
parser=Sbopen()
competitions=parser.competition()

#Preview of 'competition' dataset
print(competitions.head())
#Information about the columns of the dataset 'competitions'
competitions.info()

#Refining the 'ISL' dataset from the 'competitions' dataset
mask=competitions['competition_name'] == 'Indian Super league'
print(competitions[mask])
ISL=parser.match(competition_id=1238,season_id=108)

#Preview of the 'ISL' dataset
print(ISL.head()) 

#Refining East_Bengal FC matches from the 'ISL' dataset
mask_East_Bengal_FC= ((ISL['away_team_name'] == 'East Bengal') | (ISL['home_team_name'] == 'East Bengal'))
East_Bengal_df = ISL[mask_East_Bengal_FC]

#Creating a separate DataFrame for matches in which East_Bengal Won, Lost and Drawn
East_Bengal_df_win = pd.DataFrame()
East_Bengal_df_lose = pd.DataFrame()
East_Bengal_df_draw = pd.DataFrame()
for i,j in East_Bengal_df.iterrows():
    
    if j.iloc[15]==7286:
        if j.iloc[3]>j.iloc[4]:
            East_Bengal_df_win= East_Bengal_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[3]<j.iloc[4]:
            East_Bengal_df_lose= East_Bengal_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            East_Bengal_df_draw= East_Bengal_df_draw.append(j.to_dict(),ignore_index=True)    
    else:
        if j.iloc[4]>j.iloc[3]:
            East_Bengal_df_win= East_Bengal_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[4]<j.iloc[3]:
            East_Bengal_df_lose= East_Bengal_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            East_Bengal_df_draw= East_Bengal_df_draw.append(j.to_dict(),ignore_index=True)   

#Modifying the datatype of attribute 'match_id' in each of the above DataFrame
East_Bengal_df_win["match_id"]=East_Bengal_df_win["match_id"].astype(int)
East_Bengal_df_lose["match_id"]=East_Bengal_df_lose["match_id"].astype(int)
East_Bengal_df_draw["match_id"]=East_Bengal_df_draw["match_id"].astype(int)

#Import iterate function from network.py Script 
from East_Bengal_network import iterate

#Calling the iterate function
iterate(East_Bengal_df_win)