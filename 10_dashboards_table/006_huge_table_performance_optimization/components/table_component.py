from dash import html, dash_table
import pandas as pd
from pathlib import Path

from utils.columns_config import COLUMNS
from utils.columns_styles import style_cell_conditional

DATA_PATH = Path(__file__).resolve().parents[1] / "database" / "test_output_20000.csv"
# DATA_PATH = Path(__file__).resolve().parents[1] / "database" / "test_output_200000.csv"
test_df = pd.read_csv(DATA_PATH)

table_layout = html.Div(
    [
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

            style_table={
                "overflowY": "auto",
                "overflowX": "auto",
                "maxHeight": "70vh",
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
                "padding": "8px",
                "fontSize": "12px",
            },
            style_cell_conditional=style_cell_conditional,
        ),
    ]
)
