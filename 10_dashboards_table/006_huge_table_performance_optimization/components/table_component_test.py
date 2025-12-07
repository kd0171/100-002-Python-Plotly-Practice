# components/table_component_test.py
from dash import html, dash_table
import pandas as pd

# ---- 🔧 列10 × 行20 のテスト DataFrame ----
test_df = pd.DataFrame(
    {
        # --- 209 行のまま使える列 ---
        "A": list(range(1, 210)),
        "B": [f"b{i}" for i in range(1, 210)],
        "D": [f"d{i}" for i in range(1, 210)],
        "F": [f"f{i}" for i in range(1, 210)],
        "H": [f"h{i}" for i in range(1, 210)],
        "A2": list(range(1, 210)),
        "B2": [f"b{i}" for i in range(1, 210)],
        "D2": [f"d{i}" for i in range(1, 210)],
        "F2": [f"f{i}" for i in range(1, 210)],
        "H2": [f"h{i}" for i in range(1, 210)],

        # --- 元の仕様を維持しつつ 209 行に伸ばす列（20 行 → 209 行） ---
        "C":  (list(range(10, 210, 10)) * 11)[:209],
        "E":  (list(range(100, 2100, 100)) * 11)[:209],
        "G":  (list(range(5, 205, 10)) * 11)[:209],
        "I":  (list(range(300, 2300, 100)) * 11)[:209],
        "J":  ([f"j{i}" for i in range(1, 21)] * 11)[:209],

        "C2": (list(range(10, 210, 10)) * 11)[:209],
        "E2": (list(range(100, 2100, 100)) * 11)[:209],
        "G2": (list(range(5, 205, 10)) * 11)[:209],
        "I2": (list(range(300, 2300, 100)) * 11)[:209],
        "J2": ([f"j{i}" for i in range(1, 21)] * 11)[:209],
    }
)


table_layout_test = html.Div(
    [
        dash_table.DataTable(
            id="table-test",

            data=test_df.to_dict("records"),
            columns=[{"name": c, "id": c} for c in test_df.columns],

            # --------------------------------------
            # 🔥 固定ヘッダー + 左2列固定
            # --------------------------------------
            fixed_rows={"headers": True},
            fixed_columns={"headers": True, "data": 2},

            style_table={
                "overflowY": "auto",
                "overflowX": "auto",
                # heightとmaxHeightの両方を設定すると高さを調整可能
                "height": "80vh",          # ★ minHeight ではなく height
                "maxHeight": "80vh",          # ★ minHeight ではなく height
                "minWidth": "100%",
                "border": "1px solid lightgray",
            },

            style_cell={
                "minWidth": "120px",
                "width": "120px",
                "maxWidth": "120px",
                "textAlign": "left",
                "padding": "8px",
                "fontSize": "14px",
            },

            style_header={
                "backgroundColor": "#003963",
                "color": "white",
                "fontWeight": "bold",
                "textAlign": "center",
            },
        )
    ],
    # 🔽 外側コンテナで高さ＆枠を管理
    style={
        "width": "100%",
        "border": "1px solid lightgray" # ここに border を移動
    },
)
