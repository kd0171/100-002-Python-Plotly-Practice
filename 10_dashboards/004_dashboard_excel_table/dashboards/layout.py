# dashboards/layout.py

import os
import dash  # ★ 追加
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
                                    # ★ 全選択 / 全解除ボタンを追加
                                    dbc.Button(
                                        "全選択 / 全解除",
                                        id="apple-select-all",
                                        size="sm",
                                        color="secondary",
                                        outline=True,
                                        className="mb-2",
                                    ),
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


# ========== 2. 検索テキスト & 全選択ボタンでチェック候補/値を制御 ==========
@callback(
    Output("apple-checklist", "options"),
    Output("apple-checklist", "value"),
    Input("apple-search", "value"),
    Input("apple-select-all", "n_clicks"),
    State("apple-checklist", "options"),
    State("apple-checklist", "value"),
)
def filter_apple_checklist(search_text, select_all_clicks, current_options, current_values):
    """
    - 検索: 表示されるチェックボックスの候補だけを絞り込む（value は触らない）
    - 全選択 / 全解除ボタン:
        - 現在「表示されている候補」だけ対象
        - まだ全部選ばれていなければ「全選択」
        - すでに全部選ばれていれば「全解除」
    """
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    # 安全側初期化
    if current_values is None:
        current_values = []

    # options がまだ無い（初回など）のときは全候補
    if current_options is None or len(current_options) == 0:
        current_options = [{"label": str(v), "value": v} for v in APPLE_ALL_VALUES]

    # ===== 1. 「全選択 / 全解除」ボタンが押された場合 =====
    if triggered_id == "apple-select-all":
        # 現在表示されている候補だけ対象
        visible_values = [opt["value"] for opt in current_options]

        # 「表示されている候補すべて」がすでに選ばれていれば → それらだけ解除
        if set(visible_values).issubset(set(current_values)) and len(visible_values) > 0:
            new_values = [v for v in current_values if v not in visible_values]
        else:
            # まだ全部選ばれていない → 表示候補をすべて追加（他の選択はそのまま残す）
            new_values = list(set(current_values) | set(visible_values))

        # options は変えず、value だけ更新
        return current_options, new_values

    # ===== 2. 検索欄が変更された場合 (apple-search) =====
    # ここでは「表示候補」だけを変える。チェック状態 (value) は一切いじらない。
    if not search_text:
        filtered = APPLE_ALL_VALUES
    else:
        s = str(search_text)
        filtered = [v for v in APPLE_ALL_VALUES if s in str(v)]

    options = [{"label": str(v), "value": v} for v in filtered]

    # ★ ここが重要：
    # 以前は `current_values` を filtered に含まれるものだけに縮めていたが、
    # いまは「チェック状態は検索の影響を受けない」仕様なのでそのまま返す。
    new_values = current_values

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
