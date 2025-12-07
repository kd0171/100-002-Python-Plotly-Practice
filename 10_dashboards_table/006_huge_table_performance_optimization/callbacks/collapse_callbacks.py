# callbacks/collapse_callbacks.py
from dash import Input, Output, State


def register_collapse_callbacks(app):

    # ---------- product1 ----------
    @app.callback(
        Output("collapse-product1", "is_open"),
        Input("toggle-product1", "n_clicks"),
        State("collapse-product1", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_product1(n, is_open):
        return not is_open

    # ---------- product2 ----------
    @app.callback(
        Output("collapse-product2", "is_open"),
        Input("toggle-product2", "n_clicks"),
        State("collapse-product2", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_product2(n, is_open):
        return not is_open

    # ---------- mixed1 ----------
    @app.callback(
        Output("collapse-mixed1", "is_open"),
        Input("toggle-mixed1", "n_clicks"),
        State("collapse-mixed1", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_mixed1(n, is_open):
        return not is_open

    # ---------- quantity1 ----------
    @app.callback(
        Output("collapse-quantity1", "is_open"),
        Input("toggle-quantity1", "n_clicks"),
        State("collapse-quantity1", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_quantity1(n, is_open):
        return not is_open

    # ---------- date ----------
    @app.callback(
        Output("collapse-date", "is_open"),
        Input("toggle-date", "n_clicks"),
        State("collapse-date", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_date(n, is_open):
        return not is_open
