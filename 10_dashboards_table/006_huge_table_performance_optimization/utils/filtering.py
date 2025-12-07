# utils/filtering.py
import pandas as pd
from components.table_component import test_df

CHECKBOX_FILTER_MAP = {
    "product1": "product_1",
    "product2": "product_2",
    "mixed1": "mixed_1",
    # 今後増やしたらここに追加
}


def apply_all_filters(state, ignore_keys=None):
    df = test_df
    if state is None:
        return df

    ignore_keys = set(ignore_keys or [])

    # 1) チェックリスト系
    for key, col in CHECKBOX_FILTER_MAP.items():
        if key in ignore_keys:
            continue
        if col not in df.columns:
            continue

        val = state.get(key)
        if val in (None, "", [], "all"):
            continue

        if isinstance(val, list):
            df = df[df[col].astype(str).isin([str(v) for v in val])]
        else:
            df = df[df[col].astype(str) == str(val)]

    # 2) quantity_1 の範囲
    if "quantity1_range" not in ignore_keys:
        q_range = state.get("quantity1_range")
        if q_range and len(q_range) == 2 and "quantity_1" in df.columns:
            q_min, q_max = q_range
            q_series = pd.to_numeric(df["quantity_1"], errors="coerce")
            mask = (q_series >= q_min) & (q_series <= q_max)
            df = df[mask]

    # 3) date の範囲
    if "date_range" not in ignore_keys:
        d_range = state.get("date_range")
        if d_range and len(d_range) == 2 and "date" in df.columns:
            start_str, end_str = d_range
            dates = pd.to_datetime(df["date"], errors="coerce")
            mask = (dates >= start_str) & (dates <= end_str)
            df = df[mask]

    return df
