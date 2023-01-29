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

#Refining Jamshedpur FC matches from the 'ISL' dataset
mask_Jamshedpur_FC= ((ISL['away_team_name'] == 'Jamshedpur') | (ISL['home_team_name'] == 'Jamshedpur'))
Jamshedpur_df = ISL[mask_Jamshedpur_FC]

#Creating a separate DataFrame for matches in which Jamshedpur Won, Lost and Drawn
Jamshedpur_df_win = pd.DataFrame()
Jamshedpur_df_lose = pd.DataFrame()
Jamshedpur_df_draw = pd.DataFrame()
for i,j in Jamshedpur_df.iterrows():
    
    if j.iloc[15]==2021:
        if j.iloc[3]>j.iloc[4]:
            Jamshedpur_df_win= Jamshedpur_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[3]<j.iloc[4]:
            Jamshedpur_df_lose= Jamshedpur_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Jamshedpur_df_draw= Jamshedpur_df_draw.append(j.to_dict(),ignore_index=True)    
    else:
        if j.iloc[4]>j.iloc[3]:
            Jamshedpur_df_win= Jamshedpur_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[4]<j.iloc[3]:
            Jamshedpur_df_lose= Jamshedpur_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Jamshedpur_df_draw= Jamshedpur_df_draw.append(j.to_dict(),ignore_index=True)   

#Modifying the datatype of attribute 'match_id' in each of the above DataFrame
Jamshedpur_df_win["match_id"]=Jamshedpur_df_win["match_id"].astype(int)
Jamshedpur_df_lose["match_id"]=Jamshedpur_df_lose["match_id"].astype(int)
Jamshedpur_df_draw["match_id"]=Jamshedpur_df_draw["match_id"].astype(int)

#Import iterate function from network.py Script 
from Jamshedpur_network import iterate

#Calling the iterate function
iterate(Jamshedpur_df_draw)
