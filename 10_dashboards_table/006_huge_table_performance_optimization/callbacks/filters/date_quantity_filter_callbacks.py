# callbacks/filters/date_quantity_filter_callbacks.py
from dash import Input, Output, State
import pandas as pd

from components.table_component import test_df


def register_date_quantity_filters(app):

    # --------------------------------------------------
    # quantity_1 RangeSlider → filters-draft["quantity1_range"]
    # --------------------------------------------------
    @app.callback(
        Output("filters-draft", "data", allow_duplicate=True),
        Output("quantity1-range-display", "children"),
        Input("quantity1-range-slider", "value"),
        State("filters-draft", "data"),
        prevent_initial_call=True,
    )
    def update_quantity1_range(value, current_state):
        state = current_state or {}
        if value is None or len(value) != 2:
            state["quantity1_range"] = None
            display = "No range selected"
        else:
            q_min, q_max = float(value[0]), float(value[1])
            state["quantity1_range"] = [q_min, q_max]
            display = f"{q_min:.2f} 〜 {q_max:.2f}"

        return state, display

    # --------------------------------------------------
    # date RangeSlider → filters-draft["date_range"]
    # Slider は index ベースなので、実際の日付に変換して保存
    # --------------------------------------------------
    # DataFrame 側の日付を準備
    if "date" in test_df.columns:
        _dates = pd.to_datetime(test_df["date"], errors="coerce")
        _dates = _dates.dropna().sort_values()
        _unique_dates = _dates.dt.date.unique()
    else:
        _unique_dates = []

    @app.callback(
        Output("filters-draft", "data", allow_duplicate=True),
        Output("date-range-display", "children"),
        Input("date-range-slider", "value"),
        State("filters-draft", "data"),
        prevent_initial_call=True,
    )
    def update_date_range(idx_range, current_state):
        state = current_state or {}

        if not _unique_dates.tolist():
            state["date_range"] = None
            return state, "No date data"

        if idx_range is None or len(idx_range) != 2:
            state["date_range"] = None
            return state, "No range selected"

        start_idx, end_idx = idx_range
        start_idx = max(0, min(start_idx, len(_unique_dates) - 1))
        end_idx = max(0, min(end_idx, len(_unique_dates) - 1))

        start_date = _unique_dates[start_idx]
        end_date = _unique_dates[end_idx]

        # フィルタ用には文字列として保存
        state["date_range"] = [
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
        ]
        display = f"{start_date} 〜 {end_date}"

        return state, display
