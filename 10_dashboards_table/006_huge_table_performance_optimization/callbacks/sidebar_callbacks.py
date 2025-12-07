from dash import callback_context
from dash.dependencies import Input, Output


def register_sidebar_callbacks(app):

    @app.callback(
        [
            Output("sidebar-closed", "style"),
            Output("sidebar-opened", "style"),
            Output("table-area", "style"),
        ],
        [
            Input("sidebar-closed", "n_clicks"),
            Input("close-sidebar", "n_clicks"),
        ],
        prevent_initial_call=True,
    )
    def toggle_sidebar(open_clicks, close_clicks):

        closed_style_visible = {
            "position": "fixed",
            "top": "15%",
            "left": "0",
            "background-color": "#d3d3d3",
            "width": "40px",
            "height": "160px",
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "justify-content": "flex-start",
            "border": "2px solid #aaa",
            "border-radius": "0 5px 5px 0",
            "cursor": "pointer",
            "zIndex": 1000,
        }

        closed_style_hidden = {**closed_style_visible, "display": "none"}

        opened_style_visible = {
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "320px",
            "height": "100vh",
            "background-color": "#f8f9fa",
            "border-right": "1px solid #aaa",
            "zIndex": 999,
            "display": "block",
            "box-shadow": "2px 0 8px rgba(0,0,0,0.1)",
        }

        opened_style_hidden = {**opened_style_visible, "display": "none"}

        table_style_closed = {
            "width": "90%",
            "margin": "0 auto",
            "margin-left": "150px",
            "margin-right": "80px",
            "padding-top": "20px",
        }

        table_style_opened = {
            "width": "90%",
            "margin": "0 auto",
            "margin-left": "350px",
            "margin-right": "80px",
            "padding-top": "20px",
        }

        ctx = callback_context
        if not ctx.triggered:
            return closed_style_visible, opened_style_hidden, table_style_closed

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_id == "sidebar-closed":
            return closed_style_hidden, opened_style_visible, table_style_opened
        elif triggered_id == "close-sidebar":
            return closed_style_visible, opened_style_hidden, table_style_closed

        return closed_style_visible, opened_style_hidden, table_style_closed
