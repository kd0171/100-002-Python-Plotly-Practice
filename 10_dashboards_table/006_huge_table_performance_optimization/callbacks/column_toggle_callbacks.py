# callbacks/column_toggle_callbacks.py
from dash import Input, Output, State, callback_context

from utils.column_groups import COLUMN_GROUPS
from utils.columns_config import COLUMNS


def register_column_toggle_callbacks(app):

    # ① ボタン → column-groups-state
    @app.callback(
        Output("column-groups-state", "data"),
        [
            Input("col-group-btn-meta", "n_clicks"),
            Input("col-group-btn-products", "n_clicks"),
            Input("col-group-btn-categories", "n_clicks"),
            Input("col-group-btn-quantities", "n_clicks"),
            Input("col-group-btn-mixed", "n_clicks"),
        ],
        State("column-groups-state", "data"),
        prevent_initial_call=True,
    )
    def toggle_column_group(
        meta_clicks,
        products_clicks,
        categories_clicks,
        quantities_clicks,
        mixed_clicks,
        current_state,
    ):
        state = current_state or ["meta", "products", "categories", "quantities", "mixed"]

        ctx = callback_context
        if not ctx.triggered:
            return state

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        id_to_group = {
            "col-group-btn-meta": "meta",
            "col-group-btn-products": "products",
            "col-group-btn-categories": "categories",
            "col-group-btn-quantities": "quantities",
            "col-group-btn-mixed": "mixed",
        }

        group = id_to_group.get(triggered_id)
        if group is None:
            return state

        # トグル
        if group in state:
            state = [g for g in state if g != group]
        else:
            state = state + [group]

        return state

    # ② state → DataTable.hidden_columns
    @app.callback(
        Output("table", "hidden_columns"),
        Input("column-groups-state", "data"),
    )
    def update_hidden_columns(active_groups):
        active_groups = set(active_groups or [])
        visible = set()

        for g in active_groups:
            for col_id in COLUMN_GROUPS.get(g, []):
                visible.add(col_id)

        all_ids = [c["id"] for c in COLUMNS]
        hidden = [cid for cid in all_ids if cid not in visible]

        return hidden

    # ③ state → ボタンの濃淡（outline）
    @app.callback(
        Output("col-group-btn-meta", "outline"),
        Output("col-group-btn-products", "outline"),
        Output("col-group-btn-categories", "outline"),
        Output("col-group-btn-quantities", "outline"),
        Output("col-group-btn-mixed", "outline"),
        Input("column-groups-state", "data"),
    )
    def update_button_styles(active_groups):
        active = set(active_groups or [])
        # outline=True が「非表示（薄い）」状態
        return (
            "meta" not in active,
            "products" not in active,
            "categories" not in active,
            "quantities" not in active,
            "mixed" not in active,
        )
