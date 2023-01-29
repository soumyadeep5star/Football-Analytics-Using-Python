#Import libraries
import pandas as pd
from mplsoccer import Sbopen

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

#Refining Bengaluru FC matches from the 'ISL' dataset
mask_Bengaluru_FC= ((ISL['away_team_name'] == 'Bengaluru') | (ISL['home_team_name'] == 'Bengaluru'))
Bengaluru_df = ISL[mask_Bengaluru_FC]

#Creating a separate DataFrame for matches in which Bengaluru Won, Lost and Drawn
Bengaluru_df_win = pd.DataFrame()
Bengaluru_df_lose = pd.DataFrame()
Bengaluru_df_draw = pd.DataFrame()
for i,j in Bengaluru_df.iterrows():
    
    if j.iloc[15]==7284:
        if j.iloc[3]>j.iloc[4]:
            Bengaluru_df_win= Bengaluru_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[3]<j.iloc[4]:
            Bengaluru_df_lose= Bengaluru_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Bengaluru_df_draw= Bengaluru_df_draw.append(j.to_dict(),ignore_index=True)    
    else:
        if j.iloc[4]>j.iloc[3]:
            Bengaluru_df_win= Bengaluru_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[4]<j.iloc[3]:
            Bengaluru_df_lose= Bengaluru_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Bengaluru_df_draw= Bengaluru_df_draw.append(j.to_dict(),ignore_index=True)   

#Modifying the datatype of attribute 'match_id' in each of the above DataFrame
Bengaluru_df_win["match_id"]=Bengaluru_df_win["match_id"].astype(int)
Bengaluru_df_lose["match_id"]=Bengaluru_df_lose["match_id"].astype(int)
Bengaluru_df_draw["match_id"]=Bengaluru_df_draw["match_id"].astype(int)

#Import iterate function from Team_Name_network.py Script 
from Bengaluru_Network import iterate

#Calling the iterate function
iterate(Bengaluru_df_draw)