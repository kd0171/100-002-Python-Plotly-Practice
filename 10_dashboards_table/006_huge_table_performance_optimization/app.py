# app.py
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from components.header import header_product1
from components.table_component import table_layout
from components.sidebar_closed import sidebar_closed
from components.sidebar_opened import sidebar_opened

from callbacks.table_callbacks import register_table_callbacks
from callbacks.sidebar_callbacks import register_sidebar_callbacks
from callbacks.register_callbacks import register_all_callbacks
from utils import constants


app = Dash(
    __name__,
    title=constants.APP_MAIN_TABNAME,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# register_table_callbacks(app)
# サイドバー開閉用コールバック
register_sidebar_callbacks(app)
# フィルタ・テーブル更新用コールバック
register_all_callbacks(app)


app.layout = html.Div(
    [
        # ヘッダー
        html.Div(
            header_product1,
            style={"margin-bottom": "2%"},
        ),

        # サイドバー（閉じた状態 + 開いた状態）
        html.Div(
            [
                sidebar_closed,
                sidebar_opened,
            ]
        ),

        html.Div(
            table_layout,
            id="table-area",
            style={
                "width": "90%",
                "margin": "0 auto",
                "margin-left": "140px",
                "padding-top": "10px",
            },
        ),

        # # 👇 テスト用：画面の一番下に赤いバーを出す
        # html.Div(
        #     "ここが見えますか？",
        #     style={
        #         "height": "40px",
        #         "backgroundColor": "red",
        #         "color": "white",
        #     },
        # ),

        # フィルタ編集用（Apply 押すまでのドラフト）
        dcc.Store(id="filters-draft", storage_type="memory"),
        # 実際にテーブルに効く確定済みフィルタ
        dcc.Store(id="filters-state", storage_type="memory"),
    ]
    # ⚠ ここでは style を付けない（ページ送りが隠れないように）
)


if __name__ == "__main__":
    app.run(debug=True)
