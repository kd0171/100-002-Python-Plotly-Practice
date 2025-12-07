from dash import html, dcc
import pandas as pd

from components.table_component import test_df


def date_range_slider():
    if "date" in test_df.columns:
        dates = pd.to_datetime(test_df["date"], errors="coerce")
        dates = dates.dropna().sort_values()
        if len(dates) == 0:
            # fallback
            min_idx, max_idx = 0, 1
            marks = {0: "N/A", 1: "N/A"}
        else:
            unique_dates = dates.dt.date.unique()
            min_idx, max_idx = 0, len(unique_dates) - 1

            # マークは端＋中間くらいに
            marks = {
                0: unique_dates[0].strftime("%Y-%m-%d"),
                max_idx: unique_dates[-1].strftime("%Y-%m-%d"),
            }
            if max_idx > 2:
                mid = max_idx // 2
                marks[mid] = unique_dates[mid].strftime("%Y-%m-%d")
    else:
        min_idx, max_idx = 0, 1
        marks = {0: "N/A", 1: "N/A"}

    return html.Div(
        [
            html.Label("date range", className="form-label"),

            dcc.RangeSlider(
                id="date-range-slider",
                min=min_idx,
                max=max_idx,
                value=[min_idx, max_idx],
                step=1,
                marks=marks,
                allowCross=False,
            ),

            html.Div(
                id="date-range-display",
                style={"marginTop": "8px", "fontSize": "12px"},
            ),
        ],
        style={"padding": "10px"},
    )
