from dash import Input, Output, State
from components.table_component import test_df
from utils.filtering import apply_all_filters


def register_apply_filters(app):

    # ① Apply ボタン：draft → state
    @app.callback(
        Output("filters-state", "data"),
        Input("apply-filters-btn", "n_clicks"),
        State("filters-draft", "data"),
        prevent_initial_call=True
    )
    def commit_filters(n, draft):
        return draft or {}

    # ② table 更新（確定済みの filters-state を使用）
    @app.callback(
        Output("table", "data"),
        Input("filters-state", "data"),
        Input("table", "page_current"),
        Input("table", "page_size"),
        Input("table", "sort_by"),
    )
    def apply_filters(state, page_current, page_size, sort_by):
        df = apply_all_filters(state)

        # sort / paging
        if sort_by:
            df = df.sort_values(
                [s["column_id"] for s in sort_by],
                ascending=[s["direction"] == "asc" for s in sort_by],
            )

        page_current = page_current or 0
        page_size = page_size or 100
        start = page_current * page_size
        end = start + page_size

        return df.iloc[start:end].to_dict("records")
