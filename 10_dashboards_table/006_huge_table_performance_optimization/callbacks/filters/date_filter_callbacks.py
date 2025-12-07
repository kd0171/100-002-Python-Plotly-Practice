# callbacks/filters/date_filter_callbacks.py
from dash import Input, Output, State
import pandas as pd

from components.table_component import test_df


# モジュール読み込み時に一度だけユニーク日付を作っておく
if "date" in test_df.columns:
    _dates = pd.to_datetime(test_df["date"], errors="coerce")
    _dates = _dates.dropna().sort_values()
    _unique_dates = _dates.dt.date.unique()
else:
    _unique_dates = []


def register_date_filter(app):

    @app.callback(
        Output("filters-draft", "data", allow_duplicate=True),
        Output("date-range-display", "children"),
        Input("date-range-slider", "value"),
        State("filters-draft", "data"),
        prevent_initial_call=True,
    )
    def update_date_range(idx_range, current_state):
        """
        date 用 RangeSlider は index ベースなので、
        _unique_dates から実際の日付に変換して保存する。
        state["date_range"] = ["YYYY-MM-DD", "YYYY-MM-DD"]
        の形で filters-draft に入れる。
        """
        state = current_state or {}

        if not _unique_dates.tolist():
            state["date_range"] = None
            return state, "No date data"

        if not idx_range or len(idx_range) != 2:
            state["date_range"] = None
            return state, "No range selected"

        start_idx, end_idx = idx_range
        start_idx = max(0, min(start_idx, len(_unique_dates) - 1))
        end_idx = max(0, min(end_idx, len(_unique_dates) - 1))

        start_date = _unique_dates[start_idx]
        end_date = _unique_dates[end_idx]

        state["date_range"] = [
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
        ]

        display = f"{start_date} 〜 {end_date}"
        return state, display
