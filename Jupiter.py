import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px
from datetime import datetime
from matplotlib import offsetbox
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
df_games = pd.read_csv('Football Data/games.csv')
df_players = pd.read_csv('Football Data/players.csv')
df_clubs = pd.read_csv('Football Data/clubs.csv')
club_games = pd.read_csv("Football Data/club_games.csv")

"""# Simpliest dataframes and plots

Unpacking datasets with information about players of
the current year
"""

liga = 'RU1'
df_current_players = df_players.loc[df_players['last_season'] == 2023]
df_current_players

"""-----------------
Here we are applying League, it will be toUpperCase() in html.
"""

df_current_league_players = df_current_players.loc[df_current_players['current_club_domestic_competition_id'] == f'{liga}']

df_current_league_players.info()

"""As can be seen 👆👆👆  we shouldn't delete any rows, because missed raws aren't essential, that won't be needed in further investigation

---


**This is for making a new column - age**

With using datetime for constant updating of the information
"""

df_current_league_players['date_of_birth'] = pd.to_datetime(df_current_league_players['date_of_birth'])

current_year = datetime.now().year

df_current_league_players['age'] = current_year - df_current_league_players['date_of_birth'].dt.year

df_current_league_players['age']

"""I've done it 😎

---
It's very uncomfortable for understending transfer value, so I wanna represent it in M€
"""

df_current_league_players['market_value_in_eur'] = df_current_league_players['market_value_in_eur'].div(1000000).round(10)

"""---"""

sns.stripplot(df_current_league_players, x='age', y='market_value_in_eur',
                  hue='current_club_name', palette='Paired')

plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

st.pyplot(plt)

sns.barplot(df_current_league_players, x='age', y='market_value_in_eur').set(title=f'Relation between transfer value and age in {liga}')

st.pyplot(plt)

"""It's just an interesting fact (I can create plots)

This barplot shows us average transfer value by age

------------
Here I create a new table with total transfer value of the each team
"""

league_overview = df_current_league_players.pivot_table(index='current_club_name',  values=['market_value_in_eur'], aggfunc=sum).sort_values(by='market_value_in_eur', ascending=False)
league_overview_1 = league_overview.reset_index('current_club_name')
league_overview_1

"""**Data visualisation of this table
👀:**
"""

fig = px.bar(league_overview_1, x='current_club_name', y='market_value_in_eur',
             title=f'Total Market Value of {liga}',
             color='market_value_in_eur'
            )
fig.update_xaxes(categoryorder='total descending', tickangle=-45)


st.pyplot(plt)

"""I unpacking a new dataset with **in-season** matches. Also I immediately applying current year"""

real_matchdays = df_games[(df_games["round"].str.contains("Matchday"))]
real_matchdays

"""Believe I can dropna(), but there is no need in it. This table will be used only for merging one column)"""

RPL_matchdays = real_matchdays[real_matchdays['competition_id'] == 'RU1']
RPL_matchdays

"""-------------------


# Creating standings

-------------------
My hipothesis is: **The higher the transfer value of team, the better the result**

Unfortunately, we haven't standings. That is why I have to do it.

**1.**   If teams scored equal amount of goals, than this is a draw. If it is, apply for that match 2 (because 0-lose, 1-win).
"""

club_games.loc[club_games['own_goals'] == club_games['opponent_goals'], 'is_win'] = 2

club_games = club_games[["game_id", "club_id", "is_win"]]
club_games

"""**2.** We should create a column 'season'"""

club_games = pd.merge( club_games, real_matchdays[['game_id', 'season']])
club_games

"""**3.** Write a function which will convert values for win/lose/draw to points"""

def calculate_points(is_win):
    if is_win == 0:
        return 0
    elif is_win == 1:
        return 3
    elif is_win == 2:
        return 1
    else:
        return None

club_games['points'] = club_games['is_win'].apply(calculate_points)
club_games

"""**4.** Sum all the points by teams"""

club_seasons = club_games.groupby(["club_id", "season"], as_index=False)[['points']].sum()
club_seasons = club_seasons.loc[club_seasons['season'] == 2023]
club_seasons

"""**5.** Club_id -> club name"""

club_seasons = pd.merge(df_clubs[['club_id', 'name']], club_seasons)
club_seasons

"""---
Create a new table with columns, which are satisfied for my investigation.
"""

league_standings = club_seasons.pivot_table(index = 'name', values = 'points').sort_values(by = "points", ascending=False)
league_standings

"""Add column of market value, make correct index."""

all_data = pd.merge(league_standings, league_overview, left_index=True,right_index=True)
all_data= all_data.reset_index(names='name')
index_labels = (a for a in range(1, len(league_overview_1['current_club_name'])+1))
all_data.index = index_labels
all_data

"""This is a kludge which will help me to create nice scatterplot"""

all_data1 = all_data
index_labels = (a for a in range(len(league_overview_1['current_club_name']), 0, -1))
all_data1.index = index_labels

img = plt.imread('Football Data/Lines_On_A_Football_Pitch.jpg')
fig, ax  = plt.subplots()
ax.imshow(img, extent=[0, len(league_overview_1['current_club_name']) + 1, 0, max(all_data['market_value_in_eur'])+(max(all_data['market_value_in_eur']) * 0.05)], aspect='auto', zorder=-1)
sns.scatterplot(data=all_data, x=all_data.index, y='market_value_in_eur',
                  hue='name', palette= 'bright'
            )
plt.xlabel('place (in reverse order)')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

if liga == 'RU1':
  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Sochi.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (1, 33.200), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/akhmat.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (3, 40.450), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Baltika.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (2, 26.450), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Orenburg.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (4, 33.650), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Ural.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (5, 29.850), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Rostov.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (6, 56.600), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Fakel.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (7, 21.000), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/NN.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (8, 26.225), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Rubin.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (9, 35.200), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Spartak.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (10, 106.100), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Loko.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (11, 86.550), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/KK.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (12, 47.550), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Dinamo.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (13, 92.500), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/CSKA.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (14, 87.100), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/zenit.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (15, 145.100), frameon=False)
  ax.add_artist(ab)

  imagebox = offsetbox.OffsetImage(plt.imread('Football Data/Krasnodar.png'), zoom=0.1)
  ab = offsetbox.AnnotationBbox(imagebox, (16, 100.500), frameon=False)
  ax.add_artist(ab)

st.scatter_chart(plt)

"""---
Open new file to merge cool data
"""

league = df_clubs.loc[df_clubs['domestic_competition_id'] == f'{liga}']
current_league = league.loc[league['last_season'] == 2023]
current_league

data = pd.merge(all_data, current_league, how='right')

data

data = data[["name", 'squad_size', 'average_age', 'foreigners_percentage', 'national_team_players', 'market_value_in_eur',  'points']].sort_values(by = 'points', ascending = False)
data

sns.heatmap(data.corr(numeric_only=True),  annot=True)

st.pyplot(plt)

def desc(lig):
  if lig == "RU1":
    print(f"As can be seen, in {liga} club points depend on Transfer value. \n \n **There're some other interesting facts for {liga}:** \n 1) Club points depend on number of players from national team in the squad. \n 2) The number of players from national team for each team depends on transfer value. \n 3) The number of players from national team for each team depends on the average age of the team (the older is a team, the more national team players)")
  elif lig == "GB1":
    print(f"As can be seen, in {liga} club points depend on Transfer value. \n \n **There're some other interesting facts for {liga}:** \n 1) Club points depend on number of players from national team in the squad. \n 2) The number of players from national team for each team depends on transfer value.")
  elif lig == "IT1":
    print(f"As can be seen, in {liga} club points depend on Transfer value. \n \n **There're some other interesting facts for {liga}:** \n 1) Club points depend on number of players from national team in the squad. \n 2) The number of players from national team for each team depends on transfer value.")
  elif lig == "GR1":
    print(f"As can be seen, in {liga} club points depend on Transfer value. \n \n **There're some other interesting facts for {liga}:** \n 1) Club points depend on number of players from national team in the squad. \n 2) Club points depend on the percentage of foreigners in the club \n 3) The number of players from national team for each team depends on transfer value. \n 4) The bigger the percentage of foreigners, the older is a team  =>  foreigners are usually old \n 5) The bigger the percentage of foreigners, the more expensive the squad is")
  elif lig == 'ES1':
    print(f"As can be seen, in {liga} club points depend on Transfer value. \n \n **There're some other interesting facts for {liga}:** \n 1) Club points depend on number of players from national team in the squad. \n 2) The number of players from national team for each team depends on transfer value.")
  elif lig == 'FR1':
    print(f"As can be seen, in {liga} club points depend on Transfer value. \n \n **There're some other interesting facts for {liga}:** \n 1) Club points depend on number of players from national team in the squad. \n 2) The number of players from national team for each team depends on transfer value.")

desc(liga)
