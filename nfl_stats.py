# import packages
import nfl_data_py as nfl  # load data
import pandas as pd
import plotly.graph_objects as go


'''
How to combine data from multiple years - merge on season and use a list to make the call, the year ID is called season

pbp data is by play
roster is just the player info

so you have to specify what facet of the play you want to quantify



R/P yards cumulative by team:table
Top R/P yards by week by team:graph
Top R/P yards by week by player:graph

rpp center run
`

Questions or open items
How are penalty yards gained listed?
add in a filter by list of teams



if season specified then groupby week else group by season

'''
# Change value to not download all historic data
update = False

df_teams = nfl.import_team_desc()


years = [1999, 2000,2001] 
''',2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
         2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
'''

# wrap this in a flag

if update:

    # actual iomport calls
    df = nfl.import_pbp_data(years)
    df_players = nfl.import_rosters(years)

    # Merge in the player and team information
    df = df.merge(df_players[["player_id", "player_name", "season"]], left_on=[
        "passing_player_id", "season"], right_on=["player_id", "season"])

    # join with team table to get team color for plot
    df = df.merge(df_teams[["team_abbr", "team_color"]],
                  left_on="posteam", right_on="team_abbr")

    # remove no plays
    # df = df[df["play_type"] != "no_play"]
    df.to_csv("C:/Users/user/Documents/Code/APIs/large_data/NFL/nfl_season_out.csv")
    df.to_json(
        "C:/Users/user/Documents/Code/APIs/large_data/NFL/nfl_season_out.json")
else:
    # read in the previously downloaded data
    df = pd.read_json(
        "C:/Users/user/Documents/Code/APIs/large_data/NFL/nfl_season_out.json")


# aggregation statement to then combine things by week, player etc. Need to make this as dynamic as possible or multiple functions
'''
How do I regex for cols ending in _yds and then match those to _id player columns 

col list call but then what, may need to make an identifying mapping table


'''
df_agg = (
    df.groupby(["player_name", "team_abbr",
               "team_color", "season"], as_index=False)
    .agg({"passing_yards": "sum", "pass_touchdown": "sum", "rushing_yards": "sum", "rush_touchdown": "sum"})
)

'''
Graphing section
'''


fig = go.Figure()
for name, values in df_agg.groupby("player_name"):
    if values["passing_yards"].sum() > 10:
        fig.add_trace(
            go.Scatter(
                x=values["season"], 
                y=values["passing_yards"].cumsum(), 
                name=name, 
                mode="markers+lines", 
                line_color=values.iloc[0].team_color,
                hovertemplate=f"<b>{name}</b><br>%{{y}} yds through season %{{x}}<extra></extra>"
            )
        )
    
fig.update_layout(
    font_family="Averta, sans-serif",
    hoverlabel_font_family="Averta, sans-serif",
    xaxis_title_text="Week",
    xaxis_title_font_size=18,
    xaxis_tickfont_size=16,
    yaxis_title_text="Rushing Yards",
    yaxis_title_font_size=18,
    yaxis_tickfont_size=16,
    hoverlabel_font_size=16,
    legend_font_size=16,
    height=1000,
    width=1000
)
    
fig.show()



