from dash import html, dcc
from components.table_component import test_df


def product2_checklist():
    if "product_2" in test_df.columns:
        options = [
            {"label": str(val), "value": str(val)}
            for val in sorted(test_df["product_2"].dropna().unique())
        ]
    else:
        options = []

    return html.Div(
        [
            html.Label("product_2", className="form-label"),

            dcc.Input(
                id="product2-search-box",
                type="text",
                placeholder="Search",
                style={"width": "100%", "marginBottom": "8px"},
            ),

            html.Div(
                dcc.Checklist(
                    id="product2-checklist",
                    options=options,
                    value=[],
                    inputStyle={"marginRight": "8px"},
                    labelStyle={"display": "block", "marginBottom": "6px"},
                ),
                style={
                    "maxHeight": "180px",
                    "overflowY": "auto",
                    "border": "1px solid #ddd",
                    "borderRadius": "6px",
                    "padding": "6px",
                },
            ),
        ],
        style={"padding": "10px"},
    )
