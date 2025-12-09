# analysis/reason_category.py
"""
removal_reason 列から reason_category 列を付与するユーティリティ。

DataFrame を受け取って、"reason_category" 列を追加した DataFrame を返す。
"""

from __future__ import annotations
import pandas as pd
import numpy as np


def add_reason_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parameters
    ----------
    df : pd.DataFrame
        少なくとも 'removal_reason' 列を含む DataFrame を想定。

    Returns
    -------
    pd.DataFrame
        'reason_category' 列が追加された DataFrame。
    """

    # 元 df をそのまま書き換えたくない場合は copy()
    df = df.copy()

    # removal_reason が無いケースでも壊れないようにする
    if "removal_reason" not in df.columns:
        df["reason_category"] = np.nan
        return df

    def categorize(reason: object) -> str:
        if pd.isna(reason):
            return "unknown"

        text = str(reason).lower()

        # ★ ここは仮ルール。実データに合わせて調整してOK
        if "wear" in text or "worn" in text:
            return "wear"
        if "corrosion" in text or "rust" in text:
            return "corrosion"
        if "crack" in text or "fracture" in text:
            return "crack"
        if "overheat" in text or "over heating" in text:
            return "overheat"
        if "leak" in text:
            return "leak"
        if "vibration" in text:
            return "vibration"

        return "other"

    df["reason_category"] = df["removal_reason"].apply(categorize)

    return df
