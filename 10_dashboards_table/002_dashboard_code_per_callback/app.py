# app.py

from dash import Dash
from dashboards.layout import serve_layout

# 🔸 コールバックを持つモジュールを import（これで @callback が登録される）
import dashboards.sales_overview
import dashboards.sales_by_category_region

app = Dash(__name__)
app.layout = serve_layout

if __name__ == "__main__":
    app.run(debug=True)
