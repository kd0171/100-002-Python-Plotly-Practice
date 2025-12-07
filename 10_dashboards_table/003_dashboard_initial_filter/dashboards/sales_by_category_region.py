# dashboards/sales_by_category_region.py

from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd


def layout():
    return html.Div(
        [
            html.H2("カテゴリ × 地域 別 売上（グローバルフィルタ適用）"),

            # 1段目：カテゴリ / 地域
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("カテゴリ選択"),
                            dcc.Dropdown(
                                id="dual-category-dropdown",
                                options=[],
                                value=None,
                                clearable=True,
                                placeholder="カテゴリを選択",
                            ),
                        ],
                        style={"width": "48%"},
                    ),
                    html.Div(
                        [
                            html.Label("地域選択"),
                            dcc.Dropdown(
                                id="dual-region-dropdown",
                                options=[],
                                value=None,
                                clearable=True,
                                placeholder="地域を選択",
                            ),
                        ],
                        style={"width": "48%"},
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "gap": "10px",
                    "marginBottom": "12px",
                },
            ),

            # 2段目：軸の選択（横軸：日付種別 / 縦軸：数値項目）
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("横軸（日付）"),
                            dcc.Dropdown(
                                id="axis-date-dropdown",
                                options=[
                                    {"label": "購入日 (purchase_date)", "value": "purchase_date"},
                                    {"label": "販売日 (sales_date)", "value": "sales_date"},
                                ],
                                value="sales_date",  # デフォルトを販売日に
                                clearable=False,
                            ),
                        ],
                        style={"width": "48%"},
                    ),
                    html.Div(
                        [
                            html.Label("縦軸（数値）"),
                            dcc.Dropdown(
                                id="axis-metric-dropdown",
                                options=[
                                    {"label": "売上 (sales)", "value": "sales"},
                                    {"label": "数量 (quantity)", "value": "quantity"},
                                ],
                                value="sales",  # デフォルトを sales
                                clearable=False,
                            ),
                        ],
                        style={"width": "48%"},
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "gap": "10px",
                    "marginBottom": "12px",
                },
            ),

            dcc.Graph(
                id="dual-sales-graph",
            ),
        ],
        style={"marginTop": "30px"},
    )


@callback(
    Output("dual-sales-graph", "figure"),
    Output("dual-category-dropdown", "options"),
    Output("dual-category-dropdown", "value"),
    Output("dual-region-dropdown", "options"),
    Output("dual-region-dropdown", "value"),
    Input("filtered-data", "data"),
    Input("dual-category-dropdown", "value"),
    Input("dual-region-dropdown", "value"),
    Input("axis-date-dropdown", "value"),
    Input("axis-metric-dropdown", "value"),
)
def update_dual_sales_graph(
    filtered_records,
    selected_category,
    selected_region,
    selected_date_axis,
    selected_metric,
):
    """
    グローバルフィルタ後のデータ + 2つのローカルドロップダウン
    + 軸選択（購入日 / 販売日 ＆ sales / quantity）でグラフを更新。
    """
    # まずデータ確認
    if not filtered_records:
        empty_fig = px.bar(title="データがありません")
        return empty_fig, [], None, [], None

    df = pd.DataFrame(filtered_records)

    # 日付列を datetime に変換（文字列の場合に備えて）
    for col in ["purchase_date", "sales_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # カテゴリ / 地域の options を作成
    categories = sorted(df["category"].unique())
    regions = sorted(df["region"].unique())

    cat_options = [{"label": c, "value": c} for c in categories]
    reg_options = [{"label": r, "value": r} for r in regions]

    # 選択が有効範囲外ならリセット
    if selected_category not in categories:
        selected_category = None
    if selected_region not in regions:
        selected_region = None

    # 軸選択（おかしな値が来たときの保険）
    if selected_date_axis not in ["purchase_date", "sales_date"]:
        selected_date_axis = "sales_date"
    if selected_metric not in ["sales", "quantity"]:
        selected_metric = "sales"

    df_plot = df.copy()

    # カテゴリ / 地域でフィルタ
    if selected_category:
        df_plot = df_plot[df_plot["category"] == selected_category]
    if selected_region:
        df_plot = df_plot[df_plot["region"] == selected_region]

    if df_plot.empty:
        fig = px.bar(title="該当するデータがありません")
    else:
        # 日付 + 選択された数値で集計してもよいが、
        # まずは生データをそのまま描画（必要なら groupby に変更も可能）
        x_col = selected_date_axis
        y_col = selected_metric

        fig = px.bar(
            df_plot,
            x=x_col,
            y=y_col,
            color="product",  # 製品ごとに色分け
            title=f"カテゴリ × 地域 別 {y_col}（軸: {x_col}, フィルタ適用後）",
        )

    return fig, cat_options, selected_category, reg_options, selected_region
