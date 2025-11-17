# dashboards/filters.py

from dash import html, dcc, callback, Input, Output
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")

# 元データ（生データ）はここで一元管理
df_raw = pd.read_csv(DATA_PATH)

# 🔹 購入日・販売日を datetime に変換
df_raw["purchase_date"] = pd.to_datetime(df_raw["purchase_date"])
df_raw["sales_date"] = pd.to_datetime(df_raw["sales_date"])

# 日付スライダー用のインデックス（購入日）
purchase_min_date = df_raw["purchase_date"].min()
purchase_max_date = df_raw["purchase_date"].max()
purchase_range_days = (purchase_max_date - purchase_min_date).days

# 日付スライダー用のインデックス（販売日）
sales_min_date = df_raw["sales_date"].min()
sales_max_date = df_raw["sales_date"].max()
sales_range_days = (sales_max_date - sales_min_date).days

# 量スライダー
min_qty = int(df_raw["quantity"].min())
max_qty = int(df_raw["quantity"].max())


def layout():
    """
    グローバルフィルタ（購入日・販売日・量・会社）と
    フィルタ済みデータを保存する dcc.Store を含むレイアウト
    """
    return html.Div(
        [
            # フィルタ UI
            html.Div(
                [
                    # 🔹 購入日スライダー
                    html.Div(
                        [
                            html.Label("購入日（purchase_date）範囲"),
                            dcc.RangeSlider(
                                id="filter-purchase-date-slider",
                                min=0,
                                max=purchase_range_days,
                                value=[0, purchase_range_days],  # 全期間
                                marks={
                                    0: purchase_min_date.strftime("%Y-%m-%d"),
                                    purchase_range_days: purchase_max_date.strftime("%Y-%m-%d"),
                                },
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ],
                        style={"marginBottom": "20px"},
                    ),

                    # 🔹 販売日スライダー
                    html.Div(
                        [
                            html.Label("販売日（sales_date）範囲"),
                            dcc.RangeSlider(
                                id="filter-sales-date-slider",
                                min=0,
                                max=sales_range_days,
                                value=[0, sales_range_days],  # 全期間
                                marks={
                                    0: sales_min_date.strftime("%Y-%m-%d"),
                                    sales_range_days: sales_max_date.strftime("%Y-%m-%d"),
                                },
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ],
                        style={"marginBottom": "20px"},
                    ),

                    # 🔹 数量スライダー
                    html.Div(
                        [
                            html.Label("数量（quantity）範囲"),
                            dcc.RangeSlider(
                                id="filter-quantity-slider",
                                min=min_qty,
                                max=max_qty,
                                value=[min_qty, max_qty],
                                tooltip={"placement": "bottom", "always_visible": True},
                            ),
                        ],
                        style={"marginBottom": "20px"},
                    ),

                    # 🔹 会社名ドロップダウン
                    html.Div(
                        [
                            html.Label("会社名"),
                            dcc.Dropdown(
                                id="filter-company-dropdown",
                                options=[
                                    {"label": c, "value": c}
                                    for c in sorted(df_raw["company"].unique())
                                ],
                                value=None,      # None なら「全社」
                                clearable=True,
                                placeholder="会社を選択（未選択なら全社）",
                            ),
                        ],
                        style={"width": "300px"},
                    ),
                ],
                style={"marginBottom": "20px"},
            ),

            # フィルタ済みデータを保存するストア
            dcc.Store(id="filtered-data"),
        ]
    )


@callback(
    Output("filtered-data", "data"),
    Input("filter-purchase-date-slider", "value"),
    Input("filter-sales-date-slider", "value"),
    Input("filter-quantity-slider", "value"),
    Input("filter-company-dropdown", "value"),
)
def update_filtered_data(purchase_range, sales_range, qty_range, company):
    """
    グローバルフィルタの状態に応じて df_raw を絞り込み、
    結果を JSON (dict の list) として dcc.Store に保存。
    """

    # 🔹 購入日の範囲（スライダーのオフセット → 実日付へ）
    p_start_offset, p_end_offset = purchase_range
    p_start_date = purchase_min_date + pd.Timedelta(days=p_start_offset)
    p_end_date = purchase_min_date + pd.Timedelta(days=p_end_offset)

    # 🔹 販売日の範囲
    s_start_offset, s_end_offset = sales_range
    s_start_date = sales_min_date + pd.Timedelta(days=s_start_offset)
    s_end_date = sales_min_date + pd.Timedelta(days=s_end_offset)

    # 🔹 量の範囲
    min_q, max_q = qty_range

    df = df_raw.copy()

    df = df[
        (df["purchase_date"] >= p_start_date)
        & (df["purchase_date"] <= p_end_date)
        & (df["sales_date"] >= s_start_date)
        & (df["sales_date"] <= s_end_date)
        & (df["quantity"] >= min_q)
        & (df["quantity"] <= max_q)
    ]

    if company:
        df = df[df["company"] == company]

    # DataFrame を JSON で返す（他の callback で復元する）
    return df.to_dict("records")
