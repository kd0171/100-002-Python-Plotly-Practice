from dash import html
import dash_bootstrap_components as dbc

from components.filters.product1_checklist import product1_checklist
from components.filters.product2_checklist import product2_checklist
from components.filters.mixed1_checklist import mixed1_checklist
from components.filters.quantity1_slider import quantity1_slider
from components.filters.date_range_slider import date_range_slider
from components.filters.review_cluster_checklist import review_cluster_checklist

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

                # --- Apply Filters ボタン ---
                html.Div(
                    dbc.Button(
                        "Apply Filters",
                        id="apply-filters-btn",
                        color="primary",
                        className="mt-3",
                        style={"width": "100%"},
                    ),
                    style={"marginTop": "16px"},
                ),

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

                # product_2
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("product_2", className="filter-title"),
                                html.Span("▼", className="filter-icon"),
                            ],
                            id="toggle-product2",
                            className="filter-toggle",
                        ),
                        dbc.Collapse(
                            product2_checklist(),
                            id="collapse-product2",
                            is_open=False,
                        ),
                    ]
                ),

                # mixed_1
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("mixed_1", className="filter-title"),
                                html.Span("▼", className="filter-icon"),
                            ],
                            id="toggle-mixed1",
                            className="filter-toggle",
                        ),
                        dbc.Collapse(
                            mixed1_checklist(),
                            id="collapse-mixed1",
                            is_open=False,
                        ),
                    ]
                ),
                # ここに今後フィルターを追加していく
                # quantity_1 range
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("quantity_1", className="filter-title"),
                                html.Span("▼", className="filter-icon"),
                            ],
                            id="toggle-quantity1",
                            className="filter-toggle",
                        ),
                        dbc.Collapse(
                            quantity1_slider(),
                            id="collapse-quantity1",
                            is_open=False,
                        ),
                    ]
                ),

                # date range
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("date", className="filter-title"),
                                html.Span("▼", className="filter-icon"),
                            ],
                            id="toggle-date",
                            className="filter-toggle",
                        ),
                        dbc.Collapse(
                            date_range_slider(),
                            id="collapse-date",
                            is_open=False,
                        ),
                    ]
                ),
                # review cluster
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("Review Cluster", className="filter-title"),
                                html.Span("▼", className="filter-icon"),
                            ],
                            id="toggle-review-cluster",
                            className="filter-toggle",
                        ),
                        dbc.Collapse(
                            review_cluster_checklist(),
                            id="collapse-review-cluster",
                            is_open=False,
                        ),
                    ]
                ),
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
