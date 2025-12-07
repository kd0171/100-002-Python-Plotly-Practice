from dash import html, dcc
import pandas as pd

from components.table_component import test_df


def quantity1_slider():
    # quantity_1 を数値化して min/max を計算
    if "quantity_1" in test_df.columns:
        q = pd.to_numeric(test_df["quantity_1"], errors="coerce")
        q = q.dropna()
        if len(q) == 0:
            q_min, q_max = 0, 1
        else:
            q_min, q_max = float(q.min()), float(q.max())
    else:
        q_min, q_max = 0, 1

    return html.Div(
        [
            html.Label("quantity_1 range", className="form-label"),

            dcc.RangeSlider(
                id="quantity1-range-slider",
                min=q_min,
                max=q_max,
                value=[q_min, q_max],  # 初期は全範囲
                step=(q_max - q_min) / 100 if q_max > q_min else 1,
                tooltip={"placement": "bottom", "always_visible": False},
                allowCross=False,
            ),

            html.Div(
                id="quantity1-range-display",
                style={"marginTop": "8px", "fontSize": "12px"},
            ),
        ],
        style={"padding": "10px"},
    )
