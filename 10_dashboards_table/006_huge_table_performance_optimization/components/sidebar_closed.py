from dash import html

sidebar_closed = html.Div(
    [
        html.Div(
            "=",
            style={
                "padding": "10px 0",
                "font-size": "22px",
                "text-align": "center",
            },
        ),
        html.Div(
            "Filter",
            style={
                "writing-mode": "vertical-rl",
                "text-orientation": "sideways",
                "font-family": "Arial, sans-serif",
                "letter-spacing": "3px",
                "font-weight": "bold",
                "font-size": "20px",
                "margin-top": "30%",
                "margin-bottom": "auto",
            },
        ),
    ],
    id="sidebar-closed",
    n_clicks=0,
    style={
        "position": "fixed",
        "left": "0",
        "top": "15%",
        "background-color": "#d4d8db",
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
    },
)
