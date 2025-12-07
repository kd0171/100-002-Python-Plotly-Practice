# dashboards/layout.py

from dash import html

# セクションごとの layout() を import
from .sales_overview import layout as sales_overview_layout
from .sales_by_category_region import layout as dual_filter_layout


def serve_layout():
    """
    ページ全体のレイアウト。
    各セクションファイルの layout() を呼び出して並べるだけ。
    """
    return html.Div(
        [
            html.H1("食品販売ダッシュボード"),

            # ① シンプルなカテゴリ別売上セクション
            sales_overview_layout(),

            # ② カテゴリ × 地域セクション
            dual_filter_layout(),
        ],
        style={"margin": "30px"},
    )
