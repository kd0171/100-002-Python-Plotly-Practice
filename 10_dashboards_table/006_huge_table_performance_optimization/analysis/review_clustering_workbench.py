# analysis/review_clustering_workbench.py
"""
review 列をクラスタリングして、
- review -> cluster_id の対応表 (review_cluster_map.csv)
- クラスタのサマリー表 (review_cluster_summary.csv)
を CSV で出力する作業用スクリプト。

この CSV を Excel などで開いて、
人間が cluster_id ごとに「名前」を考えるための材料にする。
"""

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


# =========================
# 設定
# =========================
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "database" / "test_output_20000.csv"

# 出力ファイル
MAP_PATH = BASE_DIR / "database" / "review_cluster_map.csv"
SUMMARY_PATH = BASE_DIR / "database" / "review_cluster_summary.csv"

# クラスタ数（あとで変えてもOK）
N_CLUSTERS = 8

# TF-IDF のパラメータ
MAX_FEATURES = 2000
NGRAM_RANGE = (1, 2)  # 1-gram + 2-gram
MIN_DF = 2            # 2文書以上に出てくる語だけ


def main():
    # =========================
    # 1) データ読み込み
    # =========================
    df = pd.read_csv(DATA_PATH)

    if "review" not in df.columns:
        raise ValueError("CSV に 'review' 列がありません。config / generate_csv の定義を確認してください。")

    reviews = df["review"].dropna().astype(str)
    unique_reviews = reviews.unique()

    print(f"総行数: {len(df):,}")
    print(f"ユニークな review 数: {len(unique_reviews):,}")

    # =========================
    # 2) TF-IDF ベクトル化
    # =========================
    print("\n[TF-IDF] ベクトル化中...")
    vectorizer = TfidfVectorizer(
        max_features=MAX_FEATURES,
        ngram_range=NGRAM_RANGE,
        min_df=MIN_DF,
    )
    X = vectorizer.fit_transform(unique_reviews)

    print(f"TF-IDF 行列の形: {X.shape}")  # (ユニーク review 数, 語彙数)

    # =========================
    # 3) k-means クラスタリング
    # =========================
    print(f"\n[KMeans] n_clusters={N_CLUSTERS} で学習中...")
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    cluster_df = pd.DataFrame(
        {
            "review": unique_reviews,
            "cluster_id": labels,
        }
    )

    # =========================
    # 4) クラスタごとの上位単語（命名の参考）
    # =========================
    print("\n[INFO] クラスタごとの上位キーワード（名前付けの参考）")

    terms = vectorizer.get_feature_names_out()
    centers = kmeans.cluster_centers_

    topn = 8  # 各クラスタで上位何語を表示するか
    cluster_keywords = {}

    for cid in range(N_CLUSTERS):
        # 各クラスタ中心ベクトルの大きい順に上位語を取る
        center = centers[cid]
        top_idx = center.argsort()[::-1][:topn]
        keywords = [terms[i] for i in top_idx]
        cluster_keywords[cid] = keywords

        print(f"\n=== Cluster {cid} ===")
        print(", ".join(keywords))

    # =========================
    # 5) クラスタごとの代表 review 例をサマリーにまとめる
    # =========================
    summary_rows = []

    for cid in sorted(cluster_df["cluster_id"].unique()):
        sub = cluster_df[cluster_df["cluster_id"] == cid]
        count = len(sub)

        # 代表例をいくつか（Excel で見て命名しやすく）
        examples = sub["review"].head(10).tolist()  # 最大10件
        # 足りない分は空文字で埋める（列数固定のため）
        max_ex = 10
        examples += [""] * (max_ex - len(examples))

        row = {
            "cluster_id": cid,
            "count": count,
            "keywords": ", ".join(cluster_keywords[cid]),
        }
        # example_1, example_2, ... として列に展開
        for i in range(max_ex):
            row[f"example_{i+1}"] = examples[i]

        summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)

    # =========================
    # 6) CSV 出力
    # =========================
    # 6-1) 個々の review -> cluster_id の対応表
    cluster_df.to_csv(MAP_PATH, index=False)
    print(f"\n✔ review -> cluster_id 対応表を出力: {MAP_PATH}")

    # 6-2) クラスタサマリー表（キーワード + 代表例）
    summary_df.to_csv(SUMMARY_PATH, index=False)
    print(f"✔ クラスタサマリー表を出力: {SUMMARY_PATH}")

    print("\n【次のステップ】")
    print("1) review_cluster_summary.csv を Excel などで開く")
    print("2) cluster_id ごとの keywords / example_x を眺めて、分かりやすい名前を考える")
    print("3) 別途 cluster_id -> cluster_name の対応表を作る（or このスクリプトに dict で書き足す）")
    print("4) review_cluster_map.csv に cluster_name をマージして、Dash 側で review_cluster 列として利用する")


if __name__ == "__main__":
    main()
