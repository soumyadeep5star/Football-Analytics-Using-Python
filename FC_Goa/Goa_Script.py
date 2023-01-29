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

#Refining Goa FC matches from the 'ISL' dataset
mask_Goa_FC= ((ISL['away_team_name'] == 'Goa') | (ISL['home_team_name'] == 'Goa'))
Goa_df = ISL[mask_Goa_FC]

#Creating a separate DataFrame for matches in which Goa Won, Lost and Drawn
Goa_df_win = pd.DataFrame()
Goa_df_lose = pd.DataFrame()
Goa_df_draw = pd.DataFrame()
for i,j in Goa_df.iterrows():
    
    if j.iloc[15]==7288:
        if j.iloc[3]>j.iloc[4]:
            Goa_df_win= Goa_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[3]<j.iloc[4]:
            Goa_df_lose= Goa_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Goa_df_draw= Goa_df_draw.append(j.to_dict(),ignore_index=True)    
    else:
        if j.iloc[4]>j.iloc[3]:
            Goa_df_win= Goa_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[4]<j.iloc[3]:
            Goa_df_lose= Goa_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Goa_df_draw= Goa_df_draw.append(j.to_dict(),ignore_index=True)   

#Modifying the datatype of attribute 'match_id' in each of the above DataFrame
Goa_df_win["match_id"]=Goa_df_win["match_id"].astype(int)
Goa_df_lose["match_id"]=Goa_df_lose["match_id"].astype(int)
Goa_df_draw["match_id"]=Goa_df_draw["match_id"].astype(int)

#Import iterate function from Team_Name_network.py Script 
from Goa_Network import iterate

#Calling the iterate function
iterate(Goa_df_draw)