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

#Refining ATK_Mohun_Bagan FC matches from the 'ISL' dataset
mask_ATK_Mohun_Bagan_FC= ((ISL['away_team_name'] == 'ATK Mohun Bagan') | (ISL['home_team_name'] == 'ATK Mohun Bagan'))
ATK_Mohun_Bagan_df = ISL[mask_ATK_Mohun_Bagan_FC]

#Creating a separate DataFrame for matches in which ATK_Mohun_Bagan Won, Lost and Drawn
ATK_Mohun_Bagan_df_win = pd.DataFrame()
ATK_Mohun_Bagan_df_lose = pd.DataFrame()
ATK_Mohun_Bagan_df_draw = pd.DataFrame()
for i,j in ATK_Mohun_Bagan_df.iterrows():
    
    if j.iloc[15]==7282:
        if j.iloc[3]>j.iloc[4]:
            ATK_Mohun_Bagan_df_win= ATK_Mohun_Bagan_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[3]<j.iloc[4]:
            ATK_Mohun_Bagan_df_lose= ATK_Mohun_Bagan_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            ATK_Mohun_Bagan_df_draw= ATK_Mohun_Bagan_df_draw.append(j.to_dict(),ignore_index=True)    
    else:
        if j.iloc[4]>j.iloc[3]:
            ATK_Mohun_Bagan_df_win= ATK_Mohun_Bagan_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[4]<j.iloc[3]:
            ATK_Mohun_Bagan_df_lose= ATK_Mohun_Bagan_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            ATK_Mohun_Bagan_df_draw= ATK_Mohun_Bagan_df_draw.append(j.to_dict(),ignore_index=True)   

#Modifying the datatype of attribute 'match_id' in each of the above DataFrame
ATK_Mohun_Bagan_df_win["match_id"]=ATK_Mohun_Bagan_df_win["match_id"].astype(int)
ATK_Mohun_Bagan_df_lose["match_id"]=ATK_Mohun_Bagan_df_lose["match_id"].astype(int)
ATK_Mohun_Bagan_df_draw["match_id"]=ATK_Mohun_Bagan_df_draw["match_id"].astype(int)

#Import iterate function from Team_Name_network.py Script 
from ATK_Mohun_Bagan_network import iterate

#Calling the iterate function
iterate(ATK_Mohun_Bagan_df_win)