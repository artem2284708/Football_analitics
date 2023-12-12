import pandas as pd
import streamlit as st
import plotly.express as px


df_players = pd.read_csv('/Users/artem2284708/Desktop/artem/Data files/players.csv')
df_games = pd.read_csv('/Users/artem2284708/Desktop/artem/Data files/games.csv')
df_clubs = pd.read_csv('/Users/artem2284708/Desktop/artem/Data files/clubs.csv')
club_games = pd.read_csv("/Users/artem2284708/Desktop/artem/Data files/club_games.csv")

matchdays = df_games[(df_games["round"].str.contains("Matchday"))]
RPL_matchdays = matchdays[matchdays['competition_id'] == 'ES1']

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
club_seasons = pd.merge(df_clubs[['club_id', 'name']], club_seasons)

standings = club_seasons.pivot_table(index = 'name', values = 'points').sort_values(by = "points", ascending=False)
standings.reset_index()
index_labels = (a for a in range(1, len(standings['name'])+1))
standings.index = index_labels
