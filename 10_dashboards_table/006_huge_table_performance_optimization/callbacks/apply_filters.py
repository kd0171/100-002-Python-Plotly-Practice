# callbacks/apply_filters.py
from dash import Input, Output
from components.table_component import test_df


def register_apply_filters(app):

    @app.callback(
        Output("table", "data"),
        Input("filters-state", "data"),     # サイドバーのフィルタ状態
        Input("table", "page_current"),     # ページ番号
        Input("table", "page_size"),        # 1ページの行数
        Input("table", "sort_by"),          # ソート条件（custom）
    )
    def apply_filters(state, page_current, page_size, sort_by):

        # ------------- 元データ -------------
        df = test_df.copy()

        # ------------- サイドバーのフィルター適用 -------------
        if state:
            filter_map = {
                "product1": "product_1",
            }

            for key, col in filter_map.items():
                if col not in df.columns:
                    continue

                val = state.get(key)
                if val in (None, "", "all", []):
                    continue

                if isinstance(val, list):
                    df = df[df[col].astype(str).isin([str(v) for v in val])]
                else:
                    df = df[df[col].astype(str) == str(val)]

        # ------------- ソート（custom）-------------
        if sort_by:
            df = df.sort_values(
                [s["column_id"] for s in sort_by],
                ascending=[s["direction"] == "asc" for s in sort_by],
            )

        # ------------- ページング（custom）-------------
        page_current = page_current or 0
        page_size = page_size or 100

        start = page_current * page_size
        end = (page_current + 1) * page_size

        return df.iloc[start:end].to_dict("records")
