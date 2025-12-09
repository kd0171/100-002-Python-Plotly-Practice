from dash import html, dash_table
import pandas as pd
from pathlib import Path

from utils.columns_config import COLUMNS
from utils.columns_styles import style_cell_conditional

# テーブル表示日表示切替ボタン用
from components.column_toggle_bar import column_toggle_bar

DATA_PATH = Path(__file__).resolve().parents[1] / "database" / "test_output_20000.csv"
# DATA_PATH = Path(__file__).resolve().parents[1] / "database" / "test_output_200000.csv"
test_df = pd.read_csv(DATA_PATH)

table_layout = html.Div(
    [

# テーブル表示日表示切替ボタン用
        column_toggle_bar(),


        dash_table.DataTable(
            id="table",
            data=[],  # ← 初期値は空。コールバックで入れる
            columns=COLUMNS,

            # ---- ページング（custom）----
            page_action="custom",
            page_current=0,
            page_size=100,

            # ---- フィルタはサイドバー側でやる ----
            filter_action="none",

            # ---- ソートもサーバ側でやる（custom）----
            sort_action="custom",
            sort_mode="multi",
            sort_by=[],   # ← custom のときは必須

            virtualization=False,

            # ---- header固定 ----
            fixed_rows={"headers": True},
            fixed_columns={"headers": True, "data": 2},

                # ★ ここを追加 or 修正
            css=[
                {
                    "selector": ".dash-table-container",
                    "rule": "width: 100% !important; margin: 0; padding: 0;",
                },
                {
                    "selector": ".dash-spreadsheet-container .dash-spreadsheet-inner",
                    "rule": "width: 100% !important;",
                },
        # 画面左上に出る小さな Toggle Columns ボックスを消す方法
                {
                    "selector": ".show-hide",
                    "rule": "display: none;",
                }
            ],

            style_table={
                "overflowY": "auto",
                "overflowX": "auto",
                # ★これが一番重要、これをするとテーブルの大きさを変えられる
                "maxHeight": "80vh",
                "height": "80vh",   # ← 固定高さにする
                "maxWidth": "100%",
                "width": "100%",    # ← ★これを追加
            },
            style_header={
                "backgroundColor": "#003963",
                "color": "white",
                "font-size": "14px",
                "fontWeight": "400",
                "whiteSpace": "normal",
                "textAlign": "center",
            },
            style_header_conditional=[
                {
                    "if": {"header_index": 0},
                    "fontSize": "16px",
                    "fontWeight": "600",
                }
            ],
            style_cell={
                "backgroundColor": "#f2f2f2",
                "color": "#333",
                "minWidth": "140px",
                "width": "140px",      # ← 追加
                "maxWidth": "140px",   # ← 追加
                "padding": "8px",
                "fontSize": "12px",
            },
            style_cell_conditional=style_cell_conditional,
        ),
    ],
    style={"width": "100%"}   # これを付ける
)
