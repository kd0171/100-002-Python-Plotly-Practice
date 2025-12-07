# callbacks/filters/mixed1_filter_callbacks.py
from dash import Input, Output, State
from utils.filtering import apply_all_filters


def register_mixed1_filter(app):

    # ----------------------------------------------------
    # ① チェックリストの選択変化 → draft に保存
    # ----------------------------------------------------
    @app.callback(
        Output("filters-draft", "data", allow_duplicate=True),
        Input("mixed1-checklist", "value"),
        State("filters-draft", "data"),
        prevent_initial_call=True,
    )
    def update_mixed1_filter(selected_values, current_state):
        state = current_state or {}
        state["mixed1"] = selected_values or []
        return state

    # ----------------------------------------------------
    # ② options だけを更新（value には触らない！）
    #    → 参照するのは確定済み filters-state
    # ----------------------------------------------------
    @app.callback(
        Output("mixed1-checklist", "options"),
        Input("filters-state", "data"),
        Input("mixed1-search-box", "value"),
    )
    def update_mixed1_options(state, search_text):

        df = apply_all_filters(state, ignore_keys=["mixed1"])

        if "mixed_1" in df.columns:
            all_values = sorted(df["mixed_1"].dropna().unique())
        else:
            all_values = []

        if search_text and search_text.strip():
            filtered_values = [
                v for v in all_values if search_text.lower() in str(v).lower()
            ]
        else:
            filtered_values = all_values

        options = [{"label": str(v), "value": str(v)} for v in filtered_values]

        return options
