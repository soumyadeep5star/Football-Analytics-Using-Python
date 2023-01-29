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

#Refining Hyderabad FC matches from the 'ISL' dataset
mask_Hyderabad_FC= ((ISL['away_team_name'] == 'Hyderabad') | (ISL['home_team_name'] == 'Hyderabad'))
Hyderabad_df = ISL[mask_Hyderabad_FC]

#Creating a separate DataFrame for matches in which Hyderabad Won, Lost and Drawn
Hyderabad_df_win = pd.DataFrame()
Hyderabad_df_lose = pd.DataFrame()
Hyderabad_df_draw = pd.DataFrame()
for i,j in Hyderabad_df.iterrows():
    
    if j.iloc[15]==7289:        #Team id for Hyderabad FC '7289'.
        if j.iloc[3]>j.iloc[4]:
            Hyderabad_df_win= Hyderabad_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[3]<j.iloc[4]:
            Hyderabad_df_lose= Hyderabad_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Hyderabad_df_draw= Hyderabad_df_draw.append(j.to_dict(),ignore_index=True)    
    else:
        if j.iloc[4]>j.iloc[3]:
            Hyderabad_df_win= Hyderabad_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[4]<j.iloc[3]:
            Hyderabad_df_lose= Hyderabad_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Hyderabad_df_draw= Hyderabad_df_draw.append(j.to_dict(),ignore_index=True)   

#Modifying the datatype of attribute 'match_id' in each of the above DataFrame
Hyderabad_df_win["match_id"]=Hyderabad_df_win["match_id"].astype(int)
Hyderabad_df_lose["match_id"]=Hyderabad_df_lose["match_id"].astype(int)
Hyderabad_df_draw["match_id"]=Hyderabad_df_draw["match_id"].astype(int)

#Import iterate function from network.py Script 
from Hyderabad_network import iterate

#Calling the iterate function
iterate(Hyderabad_df_draw)