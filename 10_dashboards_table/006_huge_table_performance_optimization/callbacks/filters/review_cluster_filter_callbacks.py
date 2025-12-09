# callbacks/filters/review_cluster_filter_callbacks.py
from dash import Input, Output, State
from utils.filtering import apply_all_filters


def register_review_cluster_filter(app):

    # ① チェックリストの選択値 → filters-draft に保存
    @app.callback(
        Output("filters-draft", "data", allow_duplicate=True),
        Input("review-cluster-checklist", "value"),
        State("filters-draft", "data"),
        prevent_initial_call=True,
    )
    def update_review_cluster_filter(selected_values, current_state):
        state = current_state or {}
        state["review_cluster"] = selected_values or []
        return state

    # ② 他フィルタ + 検索ボックスに応じて options を更新
    @app.callback(
        Output("review-cluster-checklist", "options"),
        Output("review-cluster-checklist", "value"),
        Input("filters-draft", "data"),           # いじり途中も反映
        Input("review-cluster-search-box", "value"),
        State("review-cluster-checklist", "value"),
    )
    def update_review_cluster_options(state, search_text, current_values):

        # 自分自身（review_cluster）は無視して、他フィルタだけ適用
        df = apply_all_filters(state, ignore_keys=["review_cluster"])

        if "review_cluster" in df.columns:
            all_values = sorted(df["review_cluster"].dropna().astype(str).unique())
        else:
            all_values = []

        # 部分一致検索
        if search_text and search_text.strip():
            s = search_text.lower()
            filtered_values = [v for v in all_values if s in v.lower()]
        else:
            filtered_values = all_values

        options = [{"label": v, "value": v} for v in filtered_values]

        # 既に選ばれている値が options に存在しない場合は除外
        option_values = {opt["value"] for opt in options}
        current_values = current_values or []
        new_values = [v for v in current_values if v in option_values]

        return options, new_values
