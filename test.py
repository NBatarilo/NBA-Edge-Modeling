from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.endpoints import boxscoreadvancedv2
from nba_api.stats.endpoints import teamdashboardbygeneralsplits
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import time
import xgboost as xgb

def get_advanced_stats(game_ids):
    advanced_stats = pd.DataFrame()
    for game_id in game_ids:
        inter_advanced = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id = '0021700081')
        inter_advanced.team_stats.get_data_frame()
        time.sleep(0.6)
        
    return advanced_stats   
	
def generate_game_stats(df, teams): 
    #all_stats_arr = np.empty((30, 77, 19))
    all_teams_stats_df = pd.DataFrame()
    for i, team in enumerate(teams):
        temp_df = df[df['TEAM_NAME'] == team]
        temp_df = temp_df.sort_values(by = ['GAME_DATE'])
        temp_df = temp_df.set_index('GAME_ID')
        key_data = temp_df[['GAME_DATE', 'TEAM_NAME', 'MATCHUP', 'WL']].iloc[5:]
        temp_df = temp_df[[
           'FGM', 'FGA', 'FG_PCT', 'FG3M',
           'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
           'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS']]
        
        advanced_stats = get_advanced_stats(temp_df.index)
        
        final_organized_stats = temp_df.rolling(5).mean().shift(periods = 1).iloc[5:]#.to_dict('index')
        stats_with_key = pd.concat([final_organized_stats, key_data], axis = 1)
     
        all_teams_stats_df = pd.concat([all_teams_stats_df, stats_with_key], axis = 0)
        
    home_df = all_teams_stats_df[all_teams_stats_df['MATCHUP'].str.contains("vs.")]
    away_df = all_teams_stats_df[all_teams_stats_df['MATCHUP'].str.contains("@")]
    merged_game_stats_df = home_df.merge(away_df, on = "GAME_ID",suffixes = ("_H", "_A"))
    merged_game_stats_df = merged_game_stats_df.sort_values(by = ['GAME_DATE_H'])
      
    return merged_game_stats_df
    
    
games = leaguegamelog.LeagueGameLog(season = '2021')
df = pd.DataFrame(games.get_data_frames()[0])
teams = df['TEAM_NAME'].unique()
stats_df = generate_game_stats(df, teams)

get_advanced_stats(stats_df.index)