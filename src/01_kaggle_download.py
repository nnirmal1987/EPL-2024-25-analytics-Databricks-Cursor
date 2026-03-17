# Premier League Dataset Downloader (Simple Version)

import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

# folders
os.makedirs("footballcheck", exist_ok=True)
os.makedirs("kaggle_download", exist_ok=True)

# datasets
datasets = {
    "matches": "marcohuiii/english-premier-league-epl-match-data-2000-2025",
    "players": "eduardopalmieri/premier-league-player-stats-season-2425",
    "standings": "sattvikyadav/premier-league-2024-2025-team-statistics"
}

# connect to kaggle
api = KaggleApi()
api.authenticate()

for name, dataset in datasets.items():

    print(f"\nDownloading {name} dataset...")

    # download dataset
    api.dataset_download_files(dataset, path="kaggle_download", unzip=True)

# find csv files
files = os.listdir("kaggle_download")

for f in files:
    if f.endswith(".csv"):
        df = pd.read_csv(f"kaggle_download/{f}")

        # save to clean folder
        if "match" in f.lower():
            df.to_csv("footballcheck/matches.csv", index=False)

        elif "player" in f.lower():
            df.to_csv("footballcheck/players.csv", index=False)

        elif "team" in f.lower() or "standing" in f.lower():
            df.to_csv("footballcheck/standings.csv", index=False)

print("\n✅ Done!")
print("Files saved in ./footballcheck/")