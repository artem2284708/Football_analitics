import pandas as pd
import streamlit as st
import plotly.express as px



df_players = pd.read_csv('Data files/players.csv')
df_games = pd.read_csv('Data files/games.csv')
df_clubs = pd.read_csv('Data files/clubs.csv')
club_games = pd.read_csv("Data files/club_games.csv")


df_current_players = df_players.loc[df_players['last_season'] == 2023]
df_current_league_players = df_current_players.loc[df_current_players['current_club_domestic_competition_id'] == 'RU1']
league_overview = df_current_league_players.pivot_table(index='current_club_name',  values=['market_value_in_eur'], aggfunc=sum).sort_values(by='market_value_in_eur', ascending=False)
league_overview_1 = league_overview.reset_index('current_club_name')

fig = px.bar(league_overview_1, x='current_club_name', y='market_value_in_eur',
             title='Total Market Value of RPL',
             color='market_value_in_eur'
            )
fig.update_xaxes(categoryorder='total descending', tickangle=-45)
st.plotly_chart(fig)


matchdays = df_games[(df_games["round"].str.contains("Matchday"))]
RPL_matchdays = matchdays[matchdays['competition_id'] == 'RU1']

club_games.loc[club_games['own_goals'] == club_games['opponent_goals'], 'is_win'] = 2
club_games = club_games[["game_id", "club_id", "is_win"]]
club_games = pd.merge(RPL_matchdays[['game_id', 'season']], club_games)

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

club_seasons = club_games.groupby(["club_id", "season"], as_index=False)[['points']].sum()
club_seasons = club_seasons.loc[club_seasons['season'] == 2023]
standings = club_seasons.drop(columns=['club_id', 'season']).sort_values(by='points', ascending=False)

RPL_standings = standings.pivot_table(index = 'name', values = 'points').sort_values(by = "points", ascending=False)
RPL_standings
