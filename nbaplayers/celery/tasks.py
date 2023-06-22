from nbaplayers.celery.celery import app
from nba_api.stats.endpoints import PlayerProfileV2, CommonPlayerInfo
from nbaplayers.utils import make_csv
from nba_api.stats.endpoints import CommonAllPlayers
from celery import chord, group, chain
from pathlib import Path
from typing import Dict, List, Callable
import argparse


@app.task(name="retrieve_player_profile")
def retrieve_player_profile(player_id: int) -> Dict:
    player_stats = PlayerProfileV2(player_id)
    career_stats = player_stats.get_data_frames()[1]
    cs_dict = career_stats.to_dict(orient="records")   
    if len(cs_dict) > 0:
        current_player_stats = cs_dict[0]
    else:
        current_player_stats = {}
    return current_player_stats


@app.task(name="retrieve_player_common_info")
def retrieve_player_common_info(player_id: int) -> Dict:
    player_info = CommonPlayerInfo(player_id)
    player_info_df = player_info.get_data_frames()[0]
    players_info_records = player_info_df.to_dict(orient="records")
    if len(players_info_records) > 0:
        current_player_info = players_info_records[0]
    else:
        current_player_info = {}
    return current_player_info    


@app.task(name="insert_players_into_database")
def insert_players_into_database(player_stats: List[Dict], file_name: Path) -> None:
    player_records = [records for records in player_stats]
    fields = list(player_stats[0].keys())
    print(fields)
    make_csv(file_name, player_records, fields)


def get_all_players() -> List[Dict]:
    all_players = CommonAllPlayers()
    all_players_df = all_players.get_data_frames()[0]
    players_records = all_players_df.to_dict(orient="records")
    return players_records


@app.task(name="collect_all_player_information")
def collect_all_player_information(player_records: List[Dict], function_to_call: Callable, file_name: Path):   
    all_players_data = player_records
    player_queues = []
    for player_record in all_players_data:
        player_id = player_record['PERSON_ID']
        player_queues.append(
            function_to_call.s(player_id)
        )
    player_queues = group(player_queues)
    res = chord(player_queues, body=insert_players_into_database.s(file_name=file_name), immutable=True)
    return res

def run_player_data_collection(player_profile_csv_path: Path, player_stats_csv_path: Path):
    all_players = get_all_players()
    chn = chain(
        collect_all_player_information(all_players, retrieve_player_profile, player_stats_csv_path),
        collect_all_player_information(all_players, retrieve_player_common_info, player_profile_csv_path)
    )
    chn.delay()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--player_profile_csv_path', type=str, required=True)
    parser.add_argument('--player_stats_csv_path', type=str, required=True)
    args = parser.parse_args()
    
    player_profile_csv_path = args.player_profile_csv_path
    player_stats_csv_path = args.player_stats_csv_path
    run_player_data_collection(player_profile_csv_path, player_stats_csv_path)