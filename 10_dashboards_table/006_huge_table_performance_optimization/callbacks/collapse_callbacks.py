# callbacks/collapse_callbacks.py
from dash import Input, Output, State


def register_collapse_callbacks(app):

    # product_1 フィルターの開閉
    @app.callback(
        Output("collapse-product1", "is_open"),
        Input("toggle-product1", "n_clicks"),
        State("collapse-product1", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_product1(n, is_open):
        return not is_open
