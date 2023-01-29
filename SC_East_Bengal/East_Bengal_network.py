import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen
import pandas as pd

parser = Sbopen()


def iterate(df_1):
    sum=0
    avg=0
    count=0
    for i,j in df_1.iterrows(): #Here 'i' returns index and 'j' returns a series
        count+=1
        #Print match_id
        #print(j.iloc[0])
        
        #Find the opposition team
        if j.iloc[15]!=7286:
            opposition=j.iloc[16]
        else:
            opposition=j.iloc[28]  
        df, related, freeze, tactics = parser.event(j.iloc[0])
        
        
        #Preparation of the Data
        #check for index of first sub
        
        sub = df.loc[df["type_name"] == "Substitution"].loc[df["team_name"] == "East Bengal"].iloc[0]["index"]
        #make df with successfull passes by East_Bengal until the first substitution
        mask_East_Bengal = (df.type_name == 'Pass') & (df.team_name == "East Bengal") & (df.index < sub) & (df.outcome_name.isnull()) & (df.sub_type_name != "Throw-in")
        #taking necessary columns
        df_pass = df.loc[mask_East_Bengal, ['x', 'y', 'end_x', 'end_y', "player_name", "pass_recipient_name"]]
        #adjusting that only the surname of a player is presented.
        df_pass["player_name"] = df_pass["player_name"].apply(lambda x: str(x).split()[-1])
        df_pass["pass_recipient_name"] = df_pass["pass_recipient_name"].apply(lambda x: str(x).split()[-1])

        #Calculating vertices size and location

        scatter_df = pd.DataFrame()
        for i, name in enumerate(df_pass["player_name"].unique()):
            passx = df_pass.loc[df_pass["player_name"] == name]["x"].to_numpy()
            recx = df_pass.loc[df_pass["pass_recipient_name"] == name]["end_x"].to_numpy()
            passy = df_pass.loc[df_pass["player_name"] == name]["y"].to_numpy()
            recy = df_pass.loc[df_pass["pass_recipient_name"] == name]["end_y"].to_numpy()
            scatter_df.at[i, "player_name"] = name
            #make sure that x and y location for each circle representing the player is the average of passes and receptions
            scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
            scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
            #calculate number of passes
            scatter_df.at[i, "no"] = df_pass.loc[df_pass["player_name"] == name].count().iloc[0]

        #adjust the size of a circle so that the player who made more passes 
        scatter_df['marker_size'] = (scatter_df['no'] / scatter_df['no'].max() * 1500)

        #Calculating edge width

        #counting passes between players
        df_pass["pair_key"] = df_pass.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
        lines_df = df_pass.groupby(["pair_key"]).x.count().reset_index()
        lines_df.rename({'x':'pass_count'}, axis='columns', inplace=True)
        #setting a treshold. You can try to investigate how it changes when you change it.
        lines_df = lines_df[lines_df['pass_count']>2]

       
        
        #Plotting edges and nodes
        
        pitch = Pitch(line_color='grey',pitch_color='green')
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                            endnote_height=0.04, title_space=0, endnote_space=0)
        pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='grey', edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)
        for i, row in scatter_df.iterrows():
            pitch.annotate(row.player_name, xy=(row.x, row.y), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)
            
        for i, row in lines_df.iterrows():
                player1 = row["pair_key"].split("_")[0]
                player2 = row['pair_key'].split("_")[1]
                #take the average location of players to plot a line between them 
                player1_x = scatter_df.loc[scatter_df["player_name"] == player1]['x'].iloc[0]
                player1_y = scatter_df.loc[scatter_df["player_name"] == player1]['y'].iloc[0]
                player2_x = scatter_df.loc[scatter_df["player_name"] == player2]['x'].iloc[0]
                player2_y = scatter_df.loc[scatter_df["player_name"] == player2]['y'].iloc[0]
                num_passes = row["pass_count"]
                #adjust the line width so that the more passes, the wider the line
                line_width = (num_passes / lines_df['pass_count'].max() * 10)
                #plot lines on the pitch
                pitch.lines(player1_x, player1_y, player2_x, player2_y,
                                alpha=1, lw=line_width, zorder=2, color="white", ax = ax["pitch"])

        fig.suptitle(f"East_Bengal Passing network against {opposition}.", fontsize = 30)
        #plt.show()
        plt.savefig(f"SC East Bengal\East_Bengal_win_img/Fig_{count}")
        


        #calculate number of successful passes by player
        no_passes = df_pass.groupby(['player_name']).x.count().reset_index()
        no_passes.rename({'x':'pass_count'}, axis='columns', inplace=True)
        #print(no_passes)
        
        #find one who made most passes
        max_no = no_passes["pass_count"].max()
        #calculate the denominator - 10*the total sum of passes
        denominator = 10*no_passes["pass_count"].sum()
        #calculate the nominator
        nominator = (max_no - no_passes["pass_count"]).sum()
        #calculate the centralisation index
        centralisation_index = nominator/denominator
        print(f"Centralisation index against {opposition} is ", centralisation_index)
        sum=sum+centralisation_index
        

    print("Average Centrality index is :",sum/count)    

