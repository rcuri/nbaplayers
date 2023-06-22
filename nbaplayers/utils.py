import csv
from pathlib import Path
from typing import Dict, List
import pandas as pd

def make_csv(csv_file_path: Path, data: List[Dict], fields: List[str]) -> None:
    with open(csv_file_path, "w", newline="") as player_csv:
        writer = csv.DictWriter(player_csv, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)


def load_csv(csv_file_path: Path) -> List:
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        all_data = [row for row in csv_reader]
    return all_data

def pandas_load_csv(csv_file_path: Path) -> pd.DataFrame:
    csv_df = pd.read_csv(csv_file_path)
    return csv_df