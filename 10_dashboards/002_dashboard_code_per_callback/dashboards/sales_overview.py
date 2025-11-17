# dashboards/sales_overview.py

from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import os

# CSV のパス（絶対パス方式で安定させる）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")

df = pd.read_csv(DATA_PATH)


def layout():
    """
    1つのカテゴリドロップダウン + 売上バーグラフのセクション
    """
    return html.Div(
        [
            html.H2("カテゴリ別 売上"),

            # 🔹 ドロップダウン（id: category-dropdown）
            html.Div(
                [
                    html.Label("カテゴリ選択"),
                    dcc.Dropdown(
                        id="category-dropdown",
                        options=[
                            {"label": c, "value": c}
                            for c in sorted(df["category"].unique())
                        ],
                        value=sorted(df["category"].unique())[0],
                        clearable=False,
                    ),
                ],
                style={"width": "300px"},
            ),

            # 🔹 グラフ（id: bar-sales）
            dcc.Graph(
                id="bar-sales",
                figure=px.bar(
                    df,
                    x="product",
                    y="sales",
                    title="製品別売上（全カテゴリ）",
                ),
            ),
        ],
        style={"marginTop": "20px"},
    )


@callback(
    Output("bar-sales", "figure"),
    Input("category-dropdown", "value"),
)
def update_sales_overview(selected_category):
    """
    単一ドロップダウンでカテゴリを選んだら、
    bar-sales の figure を更新するコールバック。
    """
    if selected_category:
        filtered = df[df["category"] == selected_category]
        title = f"{selected_category} の製品別売上"
    else:
        filtered = df
        title = "製品別売上（全カテゴリ）"

    fig = px.bar(
        filtered,
        x="product",
        y="sales",
        title=title,
    )
    return fig
