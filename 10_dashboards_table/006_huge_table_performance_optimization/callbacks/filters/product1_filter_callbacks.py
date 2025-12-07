# callbacks/filters/product1_filter_callbacks.py
from dash import Input, Output, State
from utils.filtering import apply_all_filters


def register_product1_filter(app):

    # ① product1 の選択状態を filters-draft に保存
    @app.callback(
        Output("filters-draft", "data", allow_duplicate=True),
        Input("product1-checklist", "value"),
        State("filters-draft", "data"),
        prevent_initial_call=True,
    )
    def update_product1_filter(selected_values, current_state):
        state = current_state or {}
        state["product1"] = selected_values or []
        return state

    # ② 他フィルタ + 検索に応じて options だけ更新（value は触らない）
    @app.callback(
        Output("product1-checklist", "options"),
        Input("filters-state", "data"),
        Input("product1-search-box", "value"),
    )
    def update_product1_options(state, search_text):

        # 自分(product1)は ignore、他フィルタだけ適用
        df = apply_all_filters(state, ignore_keys=["product1"])

        if df is None:
            return []

        if "product_1" in df.columns:
            all_values = sorted(df["product_1"].dropna().unique())
        else:
            all_values = []

        # 検索テキストで絞り込み
        if search_text and search_text.strip():
            filtered_values = [
                v for v in all_values if search_text.lower() in str(v).lower()
            ]
        else:
            filtered_values = all_values

        options = [{"label": str(v), "value": str(v)} for v in filtered_values]
        return options
