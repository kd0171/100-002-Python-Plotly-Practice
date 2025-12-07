# dashboards/sales_overview.py

from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

def layout():
    """
    単一カテゴリ + グローバルフィルタ適用済みデータを使うセクション
    ※ ドロップダウンの options は、callback でフィルタ済みデータから決めてもよいが、
      ここではシンプルに id だけ定義しておき、
      callback 内で value を柔軟に扱う想定。
    """
    return html.Div(
        [
            html.H2("カテゴリ別 売上（グローバルフィルタ適用）"),

            html.Div(
                [
                    html.Label("カテゴリ選択"),
                    dcc.Dropdown(
                        id="category-dropdown",
                        options=[],      # options は callback でセットしてもOK
                        value=None,
                        clearable=True,
                        placeholder="カテゴリを選択（未選択なら全カテゴリ）",
                    ),
                ],
                style={"width": "300px"},
            ),

            dcc.Graph(
                id="bar-sales",
            ),
        ],
        style={"marginTop": "20px"},
    )


@callback(
    Output("bar-sales", "figure"),
    Output("category-dropdown", "options"),
    Output("category-dropdown", "value"),
    Input("filtered-data", "data"),
    Input("category-dropdown", "value"),
)
def update_sales_overview(filtered_records, selected_category):
    """
    グローバルフィルタ後のデータ（filtered-data）と
    カテゴリドロップダウンの選択値でグラフを更新。
    """
    if not filtered_records:
        # データなし
        empty_fig = px.bar(title="データがありません")
        return empty_fig, [], None

    df = pd.DataFrame(filtered_records)

    # ドロップダウン options をフィルタ済みデータから作る
    categories = sorted(df["category"].unique())
    options = [{"label": c, "value": c} for c in categories]

    # 選択されたカテゴリが範囲外になっていたらリセット
    if selected_category not in categories:
        selected_category = None

    if selected_category:
        df_plot = df[df["category"] == selected_category]
        title = f"{selected_category} の製品別売上（フィルタ適用後）"
    else:
        df_plot = df
        title = "製品別売上（全カテゴリ, フィルタ適用後）"

    fig = px.bar(
        df_plot,
        x="product",
        y="sales",
        color="company",  # 会社別着色しても面白い
        title=title,
    )

    return fig, options, selected_category
