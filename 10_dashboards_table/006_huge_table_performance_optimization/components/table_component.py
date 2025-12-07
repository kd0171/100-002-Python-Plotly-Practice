# components/table_component.py
from dash import Dash, html, dash_table
import pandas as pd
from pathlib import Path

from utils.columns_config import COLUMNS
from utils.columns_styles import style_cell_conditional

# ===== データ読込 =====
DATA_PATH = Path(__file__).resolve().parents[1] / "database" / "test_output_20000.csv"
test_df = pd.read_csv(DATA_PATH)


table_layout = html.Div(
    [
        dash_table.DataTable(
            id="table",
            data=test_df.to_dict("records"),
            columns=COLUMNS,

            # 🔹ネイティブなページ送り（必ず表示される設定）
            page_action="native",
            page_size=50,  # 1ページあたりの行数

            # # ---- ページング ----
            # page_action="custom",
            # page_current=0,
            # page_size=100,
            
            # サイドバーでフィルタするので、DataTable側のフィルタはオフ
            filter_action="none",
            sort_action="native",
            sort_mode="multi",

            # virtualization / fixed_rows はまずオフにしてシンプルに
            virtualization=False,
            # fixed_rows={"headers": True},

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
