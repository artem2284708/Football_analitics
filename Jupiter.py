import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px
import plotly.tools as tls
from datetime import datetime
from matplotlib import offsetbox
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


df_games = pd.read_csv('Football_analitics/Data files/games.csv')
df_players = pd.read_csv('Football_analitics/Data files/players.csv')
df_clubs = pd.read_csv('Football_analitics/Data files/clubs.csv')
club_games = pd.read_csv("Football_analitics/Data files/club_games.csv")


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
club_seasons
