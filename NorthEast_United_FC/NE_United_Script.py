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

#Refining NE_United FC matches from the 'ISL' dataset
mask_NE_United_FC= ((ISL['away_team_name'] == 'NorthEast United') | (ISL['home_team_name'] == 'NorthEast United'))
NE_United_df = ISL[mask_NE_United_FC]

#Creating a separate DataFrame for matches in which NE_United Won, Lost and Drawn
NE_United_df_win = pd.DataFrame()
NE_United_df_lose = pd.DataFrame()
NE_United_df_draw = pd.DataFrame()
for i,j in NE_United_df.iterrows():
    
    if j.iloc[15]==7285:
        if j.iloc[3]>j.iloc[4]:
            NE_United_df_win= NE_United_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[3]<j.iloc[4]:
            NE_United_df_lose= NE_United_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            NE_United_df_draw= NE_United_df_draw.append(j.to_dict(),ignore_index=True)    
    else:
        if j.iloc[4]>j.iloc[3]:
            NE_United_df_win= NE_United_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[4]<j.iloc[3]:
            NE_United_df_lose= NE_United_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            NE_United_df_draw= NE_United_df_draw.append(j.to_dict(),ignore_index=True)   

#Modifying the datatype of attribute 'match_id' in each of the above DataFrame
NE_United_df_win["match_id"]=NE_United_df_win["match_id"].astype(int)
NE_United_df_lose["match_id"]=NE_United_df_lose["match_id"].astype(int)
NE_United_df_draw["match_id"]=NE_United_df_draw["match_id"].astype(int)

#Import iterate function from network.py Script 
from NE_United_network import iterate

#Calling the iterate function
iterate(NE_United_df_draw)