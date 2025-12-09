# app.py
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from components.header import header_product1
from components.table_component import table_layout
# from components.table_component_test import table_layout_test as table_layout
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
            style={"margin-bottom": "2%", "flex": "0 0 auto"},
        ),

        # サイドバー（閉じた状態 + 開いた状態）
        html.Div(
            [
                sidebar_closed,
                sidebar_opened,
            ],
            style={"flex": "0 0 auto"},
        ),

        # テーブル領域（残り全部を使う）
        html.Div(
            table_layout,
            id="table-area",
            style={
                "width": "90%",
                "margin": "0 auto",
                "margin-left": "140px",
                "padding-top": "10px",
                "flex": "1 1 auto",
                "minHeight": "0",  # ★ flex 子要素が縮められるのを防ぐおまじない
            },
        ),

        dcc.Store(id="filters-draft", storage_type="memory"),
        dcc.Store(id="filters-state", storage_type="memory"),

# テーブル表示日表示切替ボタン用
        # 列グループの表示状態（例: ["meta", "products", ...]）
        dcc.Store(
            id="column-groups-state",
            storage_type="memory",
            # data=["meta", "products", "categories", "quantities", "mixed"],
            data=["products", "categories", "quantities", "mixed"],
        ),

    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh",
        "margin": 0,
    },
)



if __name__ == "__main__":
    app.run(debug=True)
