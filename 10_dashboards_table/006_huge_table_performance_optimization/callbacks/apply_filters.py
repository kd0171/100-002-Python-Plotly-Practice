# callbacks/apply_filters.py
from dash import Input, Output
from components.table_component import test_df


def register_apply_filters(app):

    @app.callback(
        Output("table", "data"),
        Input("filters-state", "data"),   # サイドバーのフィルタ状態
    )
    def apply_filters(state):

        # フィルタのたびに元データからやり直したいので copy()
        df = test_df.copy()

        # ------------- サイドバーのフィルター適用 -------------
        if state:
            # 今は product_1 のみ。増やす場合はこの map に追加
            filter_map = {
                "product1": "product_1",
                # "quantity1": "quantity_1", など
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

        # ------------- ページングはしない！ -------------
        # DataTable (page_action="native") が中で自動的にページングする
        return df.to_dict("records")
