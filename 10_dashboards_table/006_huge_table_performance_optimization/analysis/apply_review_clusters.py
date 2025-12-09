# analysis/apply_review_clusters.py
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "database" / "test_output_20000.csv"
MAP_PATH = BASE_DIR / "database" / "review_cluster_map.csv"
OUT_PATH = BASE_DIR / "database" / "test_output_20000_with_cluster.csv"

df = pd.read_csv(DATA_PATH)
cluster_map = pd.read_csv(MAP_PATH)

# review 列でマージ
df_merged = df.merge(cluster_map[["review", "cluster_name"]], on="review", how="left")

df_merged = df_merged.rename(columns={"cluster_name": "review_cluster"})
df_merged.to_csv(OUT_PATH, index=False)
print("saved:", OUT_PATH)
