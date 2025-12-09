# components/column_toggle_bar.py
from dash import html
import dash_bootstrap_components as dbc


def column_toggle_bar():
    """
    列グループ ON/OFF ボタンバー。
    active = 濃いボタン, inactive = 薄いボタン(outline) にする。
    """
    buttons = []
    for key, label in [
        ("meta", "Meta"),
        ("products", "Products"),
        ("categories", "Categories"),
        ("quantities", "Quantities"),
        ("mixed", "Mixed"),
    ]:
        buttons.append(
            dbc.Button(
                label,
                id=f"col-group-btn-{key}",
                color="primary",
                outline=False,  # 初期状態は全部表示 = 濃い
                size="sm",
                className="me-2",
            )
        )

    return html.Div(
        [
            html.Span("Columns:", style={"marginRight": "8px"}),
            dbc.ButtonGroup(buttons, size="sm"),
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "4px",
            "marginBottom": "8px",
        },
    )
