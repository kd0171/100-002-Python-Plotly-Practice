# dashboards/layout.py

from dash import html

from .filters import layout as filters_layout
from .sales_overview import layout as sales_overview_layout
from .sales_by_category_region import layout as dual_filter_layout


def serve_layout():
    """
    ページ全体のレイアウト。
    1. グローバルフィルタ
    2. グラフ1（カテゴリ別）
    3. グラフ2（カテゴリ×地域）
    """
    return html.Div(
        [
            html.H1("食品販売ダッシュボード"),

            # ① グローバルフィルタ
            filters_layout(),

            # ② 単一カテゴリの売上セクション
            sales_overview_layout(),

            # ③ カテゴリ×地域のセクション
            dual_filter_layout(),
        ],
        style={"margin": "30px"},
    )
