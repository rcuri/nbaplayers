from nbaplayers.database.base import create_db_schema
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from nbaplayers.utils import pandas_load_csv
from nbaplayers.database.player import Player
from nbaplayers.database.stat import Stat
from nbaplayers.config import DevelopmentConfig
from pathlib import Path
import pandas as pd
import argparse
from typing import Dict, List, Tuple

def extract_tables_data(player_data: List[Dict]) -> List[Tuple[Dict, Dict]]:
    player_dicts = []
    for player in player_data:
        current_player = {}
        current_player['player_id'] = player['PERSON_ID']
        current_player['player_name'] = player['DISPLAY_FIRST_LAST']
        current_player['position'] = player['POSITION']
        current_player['first_nba_season'] = player['FROM_YEAR']
        current_player['last_nba_season'] = player['TO_YEAR']
        current_player['height'] = player['HEIGHT']
        current_player['weight'] = player['WEIGHT']
        
        current_stat = {}
        current_stat['player_id'] = player['PERSON_ID']
        current_stat['field_goal_made'] = player.get('FGM', None) if player['FGM'] != '' else None
        current_stat['field_goal_attempted'] = player.get('FGA', None) if player['FGA'] != '' else None
        current_stat['field_goal_pct'] = player.get('FG_PCT', None) if player['FG_PCT'] != '' else None
        current_stat['three_pt_made'] = player.get('FG3M', None) if player['FG3M'] != '' else None
        current_stat['three_pt_attempted'] = player.get('FG3A', None) if player['FG3A'] != '' else None
        current_stat['three_pt_pct'] = player.get('FG3_PCT', None) if player['FG3_PCT'] != '' else None
        current_stat['free_throw_made'] = player.get('FTM', None) if player['FTM'] != '' else None
        current_stat['free_throw_attempted'] = player.get('FTA', None) if player['FTA'] != '' else None
        current_stat['free_throw_pct'] = player.get('FT_PCT', None) if player['FT_PCT'] != '' else None
        current_stat['points'] = player.get('PTS', None) if player['PTS'] != '' else None
        current_stat['off_reb'] = player.get('OREB', None) if player['OREB'] != '' else None
        current_stat['def_reb'] = player.get('DREB', None) if player['DREB'] != '' else None
        current_stat['tot_reb'] = player.get('REB', None) if player['REB'] != '' else None
        current_stat['assists'] = player.get('AST', None) if player['AST'] != '' else None
        current_stat['steals'] = player.get('STL', None) if player['STL'] != '' else None
        current_stat['blocks'] = player.get('BLK', None) if player['BLK'] != '' else None
        current_stat['turnovers'] = player.get('TOV', None) if player['TOV'] != '' else None
        current_stat['personal_fouls'] = player.get('PF', None) if player['PF'] != '' else None
        player_dicts.append((current_player, current_stat))
    return player_dicts


def prepare_data(profiles_csv_file_path: Path, stats_csv_file_path: Path) -> List[Tuple[Dict, Dict]]:
    profiles_csv_df = pandas_load_csv(profiles_csv_file_path)
    stats_csv_df = pandas_load_csv(stats_csv_file_path)
    merged_df = pd.merge(profiles_csv_df, stats_csv_df, on="PERSON_ID", how="outer")
    merged_records = merged_df.to_dict(orient="records")
    tables_data = extract_tables_data(merged_records)
    return tables_data


def populate_database(db_connection: str, tables_data: List[Tuple[Dict, Dict]], engine=None) -> None:
    if not engine:
        engine = create_engine(db_connection)
    create_db_schema(engine)
    with Session(engine) as session:
        for player_model_data, stat_model_data in tables_data:
            current_player_model = Player(player_model_data)
            stat_model_data['player'] = current_player_model
            current_stat_model = Stat(stat_model_data)
            session.add(current_player_model)
            session.add(current_stat_model)
        session.commit()


if __name__ == '__main__':
    db_connection = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
    parser = argparse.ArgumentParser()
    parser.add_argument('--player_profile_csv_path', type=str, required=True)
    parser.add_argument('--player_stats_csv_path', type=str, required=True)
    args = parser.parse_args()
    
    player_profile_csv_path = args.player_profile_csv_path
    player_stats_csv_path = args.player_stats_csv_path    
    csv_data = prepare_data(player_profile_csv_path, player_stats_csv_path)
    populate_database(db_connection, csv_data)

