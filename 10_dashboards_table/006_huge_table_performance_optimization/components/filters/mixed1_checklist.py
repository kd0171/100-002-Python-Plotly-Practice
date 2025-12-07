from dash import html, dcc
from components.table_component import test_df


def mixed1_checklist():
    if "mixed_1" in test_df.columns:
        options = [
            {"label": str(val), "value": str(val)}
            for val in sorted(test_df["mixed_1"].dropna().unique())
        ]
    else:
        options = []

    return html.Div(
        [
            html.Label("mixed_1", className="form-label"),

            dcc.Input(
                id="mixed1-search-box",
                type="text",
                placeholder="Search",
                style={"width": "100%", "marginBottom": "8px"},
            ),

            html.Div(
                dcc.Checklist(
                    id="mixed1-checklist",
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
