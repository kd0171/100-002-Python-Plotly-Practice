from dash import html, dcc

def category_dropdown(options):
    return html.Div([
        html.Label("カテゴリ選択"),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{"label": o, "value": o} for o in options],
            value=options[0],
            clearable=False
        ),
        html.Button("検索", id="btn-search", className="corp-btn")
    ])
