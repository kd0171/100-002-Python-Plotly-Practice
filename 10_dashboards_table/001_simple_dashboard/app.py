from dash import Dash
from dashboards.layout import serve_layout
import dashboards.callbacks  # ← コールバック読み込み（副作用の import）

app = Dash(__name__)
app.layout = serve_layout

if __name__ == "__main__":
    app.run(debug=True)
