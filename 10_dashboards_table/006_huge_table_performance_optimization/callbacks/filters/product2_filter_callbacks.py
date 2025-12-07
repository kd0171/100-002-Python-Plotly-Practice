# callbacks/filters/product2_filter_callbacks.py
from dash import Input, Output, State
from utils.filtering import apply_all_filters


def register_product2_filter(app):

    # ① product2 の選択状態を filters-draft に保存
    @app.callback(
        Output("filters-draft", "data", allow_duplicate=True),
        Input("product2-checklist", "value"),
        State("filters-draft", "data"),
        prevent_initial_call=True,
    )
    def update_product2_filter(selected_values, current_state):
        state = current_state or {}
        state["product2"] = selected_values or []
        return state

    # ② 他フィルタ + 検索に応じて options だけ更新
    @app.callback(
        Output("product2-checklist", "options"),
        Input("filters-state", "data"),
        Input("product2-search-box", "value"),
    )
    def update_product2_options(state, search_text):

        df = apply_all_filters(state, ignore_keys=["product2"])

        if df is None:
            return []

        if "product_2" in df.columns:
            all_values = sorted(df["product_2"].dropna().unique())
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
