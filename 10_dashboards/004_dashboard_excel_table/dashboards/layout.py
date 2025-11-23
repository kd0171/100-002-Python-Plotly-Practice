# dashboards/layout.py

import os
import pandas as pd
from dash import html, dash_table, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

# ======== データ読み込み（モジュールグローバル）========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sample.csv")

df = pd.read_csv(DATA_PATH, sep=";")

# Apple 列の全候補値（検索前）
APPLE_ALL_VALUES = sorted(df["Apple"].unique())


def serve_layout():
    """
    複数行ヘッダーの販売データ表
    + 「Apple 列用の Excel 風フィルタモーダル」
    """
    # 複数行ヘッダー定義
    table_columns = [
        {"name": ["", "", "Contract_Nr"],  "id": "Contract_Nr"},
        {"name": ["", "", "Buyer_name"],   "id": "Buyer_name"},
        {"name": ["", "", "Buyer_Region"], "id": "Buyer_Region"},

        {"name": ["Sold_Amount", "Fruit",     "Apple"],   "id": "Apple"},
        {"name": ["Sold_Amount", "Fruit",     "Banana"],  "id": "Banana"},
        {"name": ["Sold_Amount", "Fruit",     "Grape"],   "id": "Grape"},

        {"name": ["Sold_Amount", "Vegetable", "Tomato"],  "id": "Tomato"},
        {"name": ["Sold_Amount", "Vegetable", "Potato"],  "id": "Potato"},
        {"name": ["Sold_Amount", "Vegetable", "Carrot"],  "id": "Carrot"},
    ]

    return html.Div(
        [
            html.H1("販売データ（Excel 風モーダルフィルタ付き）"),

            # ================= ヘッダー横の「Apple フィルタ」ボタン =================
            html.Div(
                [
                    html.Span("Apple 列 ", style={"marginRight": "8px"}),
                    dbc.Button(
                        "フィルタ…",
                        id="open-apple-modal",
                        size="sm",
                        color="secondary",
                        outline=True,
                    ),
                    html.Span(
                        "（Excel の ▼ ボタンのイメージ）",
                        style={"marginLeft": "8px", "fontSize": "0.8rem", "color": "#666"},
                    ),
                ],
                style={"marginBottom": "10px"},
            ),

            # ================== Apple 用モーダル ==================
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Apple 列フィルタ")),
                    dbc.ModalBody(
                        [
                            html.Div(
                                [
                                    html.Label("検索（値でフィルタ）"),
                                    dcc.Input(
                                        id="apple-search",
                                        type="text",
                                        placeholder="例: 9 と入れると 90, 95, 98 など",
                                        style={"width": "100%", "marginBottom": "10px"},
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.Label("チェックした値だけ表示"),
                                    dcc.Checklist(
                                        id="apple-checklist",
                                        options=[
                                            {"label": str(v), "value": v}
                                            for v in APPLE_ALL_VALUES
                                        ],
                                        value=[],      # 空リスト = 全件表示として扱う
                                        inline=False,
                                        style={"maxHeight": "200px", "overflowY": "auto"},
                                    ),
                                ]
                            ),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button(
                                "閉じる（OK）",
                                id="close-apple-modal",
                                color="primary",
                                className="ms-auto",
                            )
                        ]
                    ),
                ],
                id="apple-modal",
                is_open=False,
            ),

            # ================== テーブル本体 ==================
            dash_table.DataTable(
                id="sales-table",
                columns=table_columns,
                data=df.to_dict("records"),
                merge_duplicate_headers=True,
                sort_action="native",
                filter_action="native",
                page_size=20,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center"},
            ),
        ],
        style={"margin": "30px"},
    )


# ========== 1. モーダルの開閉コールバック ==========
@callback(
    Output("apple-modal", "is_open"),
    Input("open-apple-modal", "n_clicks"),
    Input("close-apple-modal", "n_clicks"),
    State("apple-modal", "is_open"),
)
def toggle_apple_modal(open_click, close_click, is_open):
    """
    フィルタボタン or 閉じるボタンが押されたらモーダルの開閉をトグル。
    """
    if open_click or close_click:
        return not is_open
    return is_open


# ========== 2. 検索テキストでチェック候補を絞り込む ==========
@callback(
    Output("apple-checklist", "options"),
    Output("apple-checklist", "value"),
    Input("apple-search", "value"),
    State("apple-checklist", "value"),
)
def filter_apple_checklist(search_text, current_values):
    """
    検索欄に入力した文字列を含む値だけを候補として残す。
    すでにチェック済みの値のうち、候補に残っているものだけ value に維持する。
    """
    if current_values is None:
        current_values = []

    # 検索なしなら全候補
    if not search_text:
        filtered = APPLE_ALL_VALUES
    else:
        s = str(search_text)
        filtered = [v for v in APPLE_ALL_VALUES if s in str(v)]

    options = [{"label": str(v), "value": v} for v in filtered]
    new_values = [v for v in current_values if v in filtered]

    return options, new_values


# ========== 3. チェックされた値でテーブルを絞り込む ==========
@callback(
    Output("sales-table", "data"),
    Input("apple-checklist", "value"),
)
def filter_table_by_apple(selected_values):
    """
    Apple 用チェックボックスにチェックされている値だけを残して DataTable に表示。
    チェックが 0 個なら「全件表示」とする。
    """
    dff = df.copy()

    if selected_values:
        dff = dff[dff["Apple"].isin(selected_values)]

    return dff.to_dict("records")
