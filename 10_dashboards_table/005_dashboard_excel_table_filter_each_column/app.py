# app.py

from dash import Dash
from dashboards.layout import serve_layout
import dash_bootstrap_components as dbc

# Bootstrap テーマを読み込む
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = serve_layout

if __name__ == "__main__":
    app.run(debug=True)
