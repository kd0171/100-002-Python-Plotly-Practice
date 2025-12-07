import dash
from dash import Dash, html
from dash.dash_table import DataTable
import pandas as pd

df = pd.DataFrame({
    "地域_国": ["日本", "日本", "アメリカ", "ドイツ"],
    "地域_都市": ["東京", "大阪", "NY", "ベルリン"],
    "売上_数量": [100, 200, 150, 300],
    "売上_金額": [1000, 2000, 1500, 3000],
})

app = Dash(__name__)

app.layout = html.Div([
    html.H3("複数行ヘッダー（大項目 / 小項目）＋ 小項目のみフィルタ"),

    DataTable(
        id="table",
        data=df.to_dict("records"),

        # ▼ 複数行ヘッダー
        columns=[
            {"name": ["地域", "国"],    "id": "地域_国"},
            {"name": ["地域", "都市"],  "id": "地域_都市"},
            {"name": ["売上", "数量"],  "id": "売上_数量", "type": "numeric"},
            {"name": ["売上", "金額"],  "id": "売上_金額", "type": "numeric"},
        ],

        # ▼ 小項目のみ（最下層) にフィルター行が出る
        filter_action="native",

        sort_action="native",
        sort_mode="multi",

        style_table={"overflowX": "auto"},
        merge_duplicate_headers=True,
        style_header={
            "fontWeight": "bold",
            "backgroundColor": "#f0f0f0",
            "textAlign": "center"
        },
        style_cell={"padding": "5px"},
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
