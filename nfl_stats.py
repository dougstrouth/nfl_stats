# import packages
import nfl_data_py as nfl  # load data
import pandas as pd
import plotly.graph_objects as go


'''
How to combine data from multiple years

pbp data is by play
roster is just the player info

so you have to specify what facet of the play you want to quantify



'''




df_teams = nfl.import_team_desc()



year1 =1999 
year2 =2020


main_df = {}


while year1<=year2:
    df = nfl.import_pbp_data([year1])
    df_players = nfl.import_rosters([year1])

    year1+=1


v


'''column_names = df.columns.values.tolist()
print(column_names)

column_names = df_players.columns.values.tolist()
print(column_names)
'''


df = df.merge(df_players[["player_id", "player_name"]], left_on="rusher_player_id", right_on="player_id")
# join with team table to get team color for plot
df = df.merge(df_teams[["team_abbr", "team_color"]], left_on="posteam", right_on="team_abbr")

# remove no plays
df = df[df["play_type"] != "no_play"]
df.to_csv("C:/Users/user/Documents/Code/APIs/large_data/NFL/"+str(year)+'_nfl_season_out.csv')  






df_agg = (
    df.groupby(["player_name", "team_abbr", "team_color", "week"], as_index=False)
    .agg({"passing_yards": "sum", "pass_touchdown": "sum", "rushing_yards":"sum","rush_touchdown":"sum"})
)

print(df_agg)


fig = go.Figure()
for name, values in df_agg.groupby("player_name"):
    if values["rushing_yards"].sum() > 1000:
        fig.add_trace(
            go.Scatter(
                x=values["week"], 
                y=values["rushing_yards"].cumsum(), 
                name=name, 
                mode="markers+lines", 
                line_color=values.iloc[0].team_color,
                hovertemplate=f"<b>{name}</b><br>%{{y}} yds through week %{{x}}<extra></extra>"
            )
        )
    
fig.update_layout(
    font_family="Averta, sans-serif",
    hoverlabel_font_family="Averta, sans-serif",
    xaxis_title_text="Week",
    xaxis_title_font_size=18,
    xaxis_tickfont_size=16,
    yaxis_title_text="Passing Yards",
    yaxis_title_font_size=18,
    yaxis_tickfont_size=16,
    hoverlabel_font_size=16,
    legend_font_size=16,
    height=1000,
    width=1000
)
    
fig.show()