import random
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "database" / "test_output_20000.csv"
REVIEW_MASTER_PATH = BASE_DIR / "database" / "review_master.csv"
OUT_PATH = BASE_DIR / "database" / "test_output_20000_with_review.csv"


def main() -> None:
    # --- 元データ ---
    df = pd.read_csv(DATA_PATH)

    # --- 一意レビュー一覧（DISTINCT の結果を想定）---
    review_master = pd.read_csv(REVIEW_MASTER_PATH)

    # カラム名は "review" 想定。違う場合はここを変える
    unique_reviews = (
        review_master["review"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if not unique_reviews:
        raise ValueError("review_master に有効なレビューがありません")

    # --- 行ごとにレビューを割り当て ---
    # ここでは「ランダムに割り振り」。偏りを抑えたいなら後ろで別案を説明します。
    random.seed(42)  # 再現性のための seed（お好みで）
    df["review"] = [
        random.choice(unique_reviews)
        for _ in range(len(df))
    ]

    # 保存
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"✅ review 列を付与して保存しました: {OUT_PATH}")


if __name__ == "__main__":
    main()
