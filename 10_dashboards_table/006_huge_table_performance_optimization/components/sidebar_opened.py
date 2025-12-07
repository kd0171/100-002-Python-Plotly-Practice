from dash import html
import dash_bootstrap_components as dbc

from components.filters.product1_checklist import product1_checklist


sidebar_opened = html.Div(
    [
        dbc.Button(
            "X",
            id="close-sidebar",
            className="close-sidebar-btn",
            size="sm",
        ),

        html.Div(
            [
                html.H6("FILTERED BY", className="mt-4"),

                # product_1
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("product_1", className="filter-title"),
                                html.Span("▼", className="filter-icon"),
                            ],
                            id="toggle-product1",
                            className="filter-toggle",
                        ),
                        dbc.Collapse(
                            product1_checklist(),
                            id="collapse-product1",
                            is_open=False,
                        ),
                    ]
                ),

                # ここに今後フィルターを追加していく
            ],
            className="sidebar-content",
            style={
                "height": "100vh",
                "overflowY": "auto",
                "overflowX": "hidden",
                "direction": "ltr",
                "padding": "1rem",
            },
        ),
    ],
    id="sidebar-opened",
    className="sidebar-opened",
    style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "width": "320px",
        "height": "100vh",
        "backgroundColor": "#fff",
        "borderLeft": "1px solid #ddd",
        "display": "none",
        "flexDirection": "column",
        "zIndex": "1040",
    },
)
