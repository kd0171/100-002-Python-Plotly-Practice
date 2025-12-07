# callbacks/table_callbacks.py

from dash import Input, Output
from components.table_component import test_df

def register_table_callbacks(app):
    @app.callback(  # ← ここが重要！
        Output("table", "data"),
        Input("table", "page_current"),
        Input("table", "page_size"),
        prevent_initial_call=True,
    )
    def update_table(page_current, page_size):
        start = page_current * page_size
        end = (page_current + 1) * page_size
        return test_df.iloc[start:end].to_dict("records")
