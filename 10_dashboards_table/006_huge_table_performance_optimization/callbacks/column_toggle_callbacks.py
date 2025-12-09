# callbacks/column_toggle_callbacks.py
from dash import Input, Output, State, callback_context

from utils.column_groups import COLUMN_GROUPS, META_COLUMNS
from utils.columns_config import COLUMNS


def register_column_toggle_callbacks(app):

    # ① ボタン → column-groups-state
    # ------------------------------------------------------------
    # ★ 変更ポイント
    #   - 以前は meta もトグル対象だったが、
    #     「Meta は常に表示」にしたので Input から除外。
    #   - state の初期値からも "meta" を削除。
    # ------------------------------------------------------------
    @app.callback(
        Output("column-groups-state", "data"),
        [
            # 旧: Meta もトグル対象
            # Input("col-group-btn-meta", "n_clicks"),
            Input("col-group-btn-products", "n_clicks"),
            Input("col-group-btn-categories", "n_clicks"),
            Input("col-group-btn-quantities", "n_clicks"),
            Input("col-group-btn-mixed", "n_clicks"),
        ],
        State("column-groups-state", "data"),
        prevent_initial_call=True,
    )
    def toggle_column_group(
        # 旧:
        # meta_clicks,
        products_clicks,
        categories_clicks,
        quantities_clicks,
        mixed_clicks,
        current_state,
    ):
        # 旧: state = current_state or ["meta", "products", "categories", "quantities", "mixed"]
        # Meta は常に表示にするので、state では管理しない
        state = current_state or ["products", "categories", "quantities", "mixed"]

        ctx = callback_context
        if not ctx.triggered:
            return state

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # 旧: Meta も含めていた id_to_group
        # id_to_group = {
        #     "col-group-btn-meta": "meta",
        #     "col-group-btn-products": "products",
        #     "col-group-btn-categories": "categories",
        #     "col-group-btn-quantities": "quantities",
        #     "col-group-btn-mixed": "mixed",
        # }

        # 新: Meta はトグルしないので対応表から除外
        id_to_group = {
            "col-group-btn-products": "products",
            "col-group-btn-categories": "categories",
            "col-group-btn-quantities": "quantities",
            "col-group-btn-mixed": "mixed",
        }

        group = id_to_group.get(triggered_id)
        if group is None:
            return state

        # トグル（ON → OFF / OFF → ON）
        if group in state:
            state = [g for g in state if g != group]
        else:
            state = state + [group]

        return state

    # ② state → DataTable.hidden_columns
    # ------------------------------------------------------------
    # ★ Meta は常に表示したいので、
    #   初期の visible に META_COLUMNS（["id", "date"]）を入れておく。
    #   これにより、どのグループを OFF にしても Meta は隠れない。
    # ------------------------------------------------------------
    @app.callback(
        Output("table", "hidden_columns"),
        Input("column-groups-state", "data"),
    )
    def update_hidden_columns(active_groups):
        active_groups = set(active_groups or [])

        # Meta 列は常に可視
        visible = set(META_COLUMNS)

        # 有効なグループの列を visible に追加
        for g in active_groups:
            for col_id in COLUMN_GROUPS.get(g, []):
                visible.add(col_id)

        # 全列 id から visible 以外を hidden として返す
        all_ids = [c["id"] for c in COLUMNS]
        hidden = [cid for cid in all_ids if cid not in visible]

        return hidden

    # ③ state → ボタンの濃淡（outline）
    # ------------------------------------------------------------
    # ★ 変更ポイント
    #   - 以前は Meta ボタンも outline を制御していたが、
    #     Meta は常に表示＆トグルしない前提なので対象から外す。
    #   - Meta 用の Output と戻り値を削除。
    #   - （もし UI 側に Meta ボタンが残っていても、
    #      「常に濃く表示したい」なら outline=False 固定の callback を
    #      別に一つ定義する形でも OK）
    # ------------------------------------------------------------
    @app.callback(
        # 旧:
        # Output("col-group-btn-meta", "outline"),
        Output("col-group-btn-products", "outline"),
        Output("col-group-btn-categories", "outline"),
        Output("col-group-btn-quantities", "outline"),
        Output("col-group-btn-mixed", "outline"),
        Input("column-groups-state", "data"),
    )
    def update_button_styles(active_groups):
        active = set(active_groups or [])

        # outline=True が「非表示（薄い）」状態
        # 旧: 先頭に "meta" 用の判定があった
        # return (
        #     "meta" not in active,
        #     "products" not in active,
        #     "categories" not in active,
        #     "quantities" not in active,
        #     "mixed" not in active,
        # )

        return (
            "products" not in active,
            "categories" not in active,
            "quantities" not in active,
            "mixed" not in active,
        )
