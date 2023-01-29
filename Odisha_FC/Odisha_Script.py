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

#Refining Odisha FC matches from the 'ISL' dataset
mask_Odisha_FC= ((ISL['away_team_name'] == 'Odisha') | (ISL['home_team_name'] == 'Odisha'))
Odisha_df = ISL[mask_Odisha_FC]

#Creating a separate DataFrame for matches in which Odisha Won, Lost and Drawn
Odisha_df_win = pd.DataFrame()
Odisha_df_lose = pd.DataFrame()
Odisha_df_draw = pd.DataFrame()
for i,j in Odisha_df.iterrows():
    
    if j.iloc[15]==7291:
        if j.iloc[3]>j.iloc[4]:
            Odisha_df_win= Odisha_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[3]<j.iloc[4]:
            Odisha_df_lose= Odisha_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Odisha_df_draw= Odisha_df_draw.append(j.to_dict(),ignore_index=True)    
    else:
        if j.iloc[4]>j.iloc[3]:
            Odisha_df_win= Odisha_df_win.append(j.to_dict(),ignore_index=True)
        elif j.iloc[4]<j.iloc[3]:
            Odisha_df_lose= Odisha_df_lose.append(j.to_dict(),ignore_index=True)
        else:
            Odisha_df_draw= Odisha_df_draw.append(j.to_dict(),ignore_index=True)   

#Modifying the datatype of attribute 'match_id' in each of the above DataFrame
Odisha_df_win["match_id"]=Odisha_df_win["match_id"].astype(int)
Odisha_df_lose["match_id"]=Odisha_df_lose["match_id"].astype(int)
Odisha_df_draw["match_id"]=Odisha_df_draw["match_id"].astype(int)

#Import iterate function from Team_Name_network.py Script 
from Odisha_Network import iterate

#Calling the iterate function
iterate(Odisha_df_lose)