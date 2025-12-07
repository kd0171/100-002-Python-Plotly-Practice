# app.py

from dash import Dash
import dash_bootstrap_components as dbc
from dashboards.layout import serve_layout  # ← あなたの layout.py の関数

# suppress_callback_exceptions=True を付ける
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# layout は「関数」をそのまま渡す（セッションごとに再評価されるスタイル）
app.layout = serve_layout

# Dash に「全コンポーネントが揃った完成版レイアウト」を教えておく
# これがないと、動的レイアウト時に ID not found が出やすい
app.validation_layout = serve_layout()

if __name__ == "__main__":
    app.run(debug=True)
