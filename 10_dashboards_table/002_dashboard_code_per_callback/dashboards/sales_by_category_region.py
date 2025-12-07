# dashboards/sales_by_category_region.py

from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")

df = pd.read_csv(DATA_PATH)


def layout():
    """
    2つのドロップダウン（カテゴリ・地域）＋グラフのセクション。
    """
    return html.Div(
        [
            html.H2("カテゴリ × 地域 別 売上"),

            html.Div(
                [
                    # カテゴリ選択
                    html.Div(
                        [
                            html.Label("カテゴリ選択"),
                            dcc.Dropdown(
                                id="dual-category-dropdown",
                                options=[
                                    {"label": c, "value": c}
                                    for c in sorted(df["category"].unique())
                                ],
                                value=sorted(df["category"].unique())[0],
                                clearable=False,
                            ),
                        ],
                        style={"width": "48%"},
                    ),
                    # 地域選択
                    html.Div(
                        [
                            html.Label("地域選択"),
                            dcc.Dropdown(
                                id="dual-region-dropdown",
                                options=[
                                    {"label": r, "value": r}
                                    for r in sorted(df["region"].unique())
                                ],
                                value=sorted(df["region"].unique())[0],
                                clearable=False,
                            ),
                        ],
                        style={"width": "48%"},
                    ),
                ],
                style={"display": "flex", "justifyContent": "space-between", "gap": "10px"},
            ),

            dcc.Graph(
                id="dual-sales-graph",
                figure=px.bar(
                    df,
                    x="product",
                    y="sales",
                    title="カテゴリ × 地域 別 売上",
                ),
            ),
        ],
        style={"marginTop": "30px"},
    )


@callback(
    Output("dual-sales-graph", "figure"),
    Input("dual-category-dropdown", "value"),
    Input("dual-region-dropdown", "value"),
)
def update_dual_sales_graph(selected_category, selected_region):
    """
    カテゴリ＋地域の2つのドロップダウンから選択された値で、
    dual-sales-graph の figure を更新する。
    """
    filtered = df.copy()

    if selected_category:
        filtered = filtered[filtered["category"] == selected_category]

    if selected_region:
        filtered = filtered[filtered["region"] == selected_region]

    if filtered.empty:
        fig = px.bar(title="該当するデータがありません")
    else:
        fig = px.bar(
            filtered,
            x="product",
            y="sales",
            title=f"{selected_category} × {selected_region} の製品別売上",
        )

    return fig
