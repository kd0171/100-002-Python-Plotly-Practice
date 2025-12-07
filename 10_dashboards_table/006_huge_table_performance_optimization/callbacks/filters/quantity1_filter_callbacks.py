# callbacks/filters/quantity1_filter_callbacks.py
from dash import Input, Output, State


def register_quantity1_filter(app):

    @app.callback(
        Output("filters-draft", "data", allow_duplicate=True),
        Output("quantity1-range-display", "children"),
        Input("quantity1-range-slider", "value"),
        State("filters-draft", "data"),
        prevent_initial_call=True,
    )
    def update_quantity1_range(value, current_state):
        """
        quantity_1 の RangeSlider の値を filters-draft に保存しつつ、
        下にレンジ表示用のテキストも更新する。
        state["quantity1_range"] = [min, max] という形で保存。
        """
        state = current_state or {}

        if not value or len(value) != 2:
            state["quantity1_range"] = None
            return state, "No range selected"

        q_min, q_max = float(value[0]), float(value[1])
        state["quantity1_range"] = [q_min, q_max]

        display = f"{q_min:.2f} 〜 {q_max:.2f}"
        return state, display
