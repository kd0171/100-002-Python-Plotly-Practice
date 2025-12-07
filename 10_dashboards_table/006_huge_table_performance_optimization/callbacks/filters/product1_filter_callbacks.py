from dash import Input, Output, State
from components.table_component import test_df


# ① product_1 の選択状態を filters-state に保存
def register_product1_filter(app):

    @app.callback(
        Output("filters-state", "data", allow_duplicate=True),
        Input("product1-checklist", "value"),
        State("filters-state", "data"),
        prevent_initial_call=True,
    )
    def update_product1_filter(selected_values, current_state):
        state = current_state or {}
        state["product1"] = selected_values or []
        return state


# ② 他フィルタとの組合せ + 検索で options/value を更新
def register_product1_combined(app):

    @app.callback(
        Output("product1-checklist", "options"),
        Output("product1-checklist", "value"),
        Input("filters-state", "data"),
        Input("product1-search-box", "value"),
        State("product1-checklist", "value"),
    )
    def update_product1_options(state, search_text, current_values):

        df = test_df.copy()

        # 将来 他フィルタもここに追加していく想定
        filter_map = {
            "product1": "product_1",
            # "flag": "flag_column_name",
            # "env": "env_column_name",
        }

        # ★ポイント：
        # options を作るときは「自分自身(product1)」のフィルタは無視する
        if state:
            for key, col in filter_map.items():
                if key == "product1":
                    continue  # ← 自分自身はスキップ

                val = state.get(key)
                if val not in (None, "", "all", []):
                    if isinstance(val, list):
                        df = df[df[col].astype(str).isin([str(v) for v in val])]
                    else:
                        df = df[df[col].astype(str) == str(val)]

        # 値一覧（他フィルタだけ反映された状態）
        if "product_1" in df.columns:
            all_values = sorted(df["product_1"].dropna().unique())
        else:
            all_values = []

        # 部分一致検索
        if search_text and search_text.strip():
            filtered_values = [
                v for v in all_values if search_text.lower() in str(v).lower()
            ]
        else:
            filtered_values = all_values

        options = [{"label": str(v), "value": str(v)} for v in filtered_values]

        # 現在選択されている値のうち、まだ options に残っているものだけ維持
        option_values = {opt["value"] for opt in options}
        current_values = current_values or []
        new_values = [v for v in current_values if v in option_values]

        return options, new_values
