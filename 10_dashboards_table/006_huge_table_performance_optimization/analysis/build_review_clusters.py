# analysis/build_review_clusters.py
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "database" / "test_output_20000.csv"

df = pd.read_csv(DATA_PATH)

# 1) review のユニークな表現だけ取り出す
reviews = df["review"].dropna().astype(str)
unique_reviews = reviews.unique()

# 2) TF-IDF ベクトル化
vectorizer = TfidfVectorizer(
    max_features=2000,
    ngram_range=(1, 2),  # 1-gram + 2-gram くらいが短文には相性よい
    min_df=2,            # 2回以上出た語だけ
)
X = vectorizer.fit_transform(unique_reviews)

# 3) k-means クラスタリング
k = 8  # ★ クラスタ数はあとで調整する
kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
labels = kmeans.fit_predict(X)

cluster_df = pd.DataFrame(
    {
        "review": unique_reviews,
        "cluster_id": labels,
    }
)

# 4) クラスタごとにサンプルを眺めて、人間が名前を決めるための補助
for cid in sorted(cluster_df["cluster_id"].unique()):
    examples = cluster_df[cluster_df["cluster_id"] == cid]["review"].head(8).tolist()
    print(f"\n=== Cluster {cid} ===")
    for ex in examples:
        print(" -", ex)

# 5) 人間が決めた名前を後から手で付ける想定
#   例: {0: "high performance", 1: "frequent issues", ...}
cluster_name_map = {
    0: "high performance",
    1: "frequent issues",
    2: "maintenance needed",
    3: "good value",
    4: "installation difficult",
    5: "no major issues",
    6: "noisy",
    7: "great support",
}

cluster_df["cluster_name"] = cluster_df["cluster_id"].map(cluster_name_map)

# 6) 対応表を保存（review -> cluster_name）
OUT_PATH = BASE_DIR / "database" / "review_cluster_map.csv"
cluster_df.to_csv(OUT_PATH, index=False)
print("saved:", OUT_PATH)
