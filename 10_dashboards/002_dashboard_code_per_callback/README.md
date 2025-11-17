# Dash アプリ全体の流れと連携の仕組み（README）

## 0. 全体像（ざっくり）

Dash アプリはざっくりいうと：

-   **layout**\
    →
    画面に「どんなコンポーネント（パーツ）を、どの順番で置くか」を定義する

-   **callback**\
    → 「どのパーツが変わったら、どのパーツをどう更新するか」を定義する\
    → Input(id, prop) と Output(id, prop) をつなぐ

-   **app.py**\
    → Dash 本体を作って\
    → layout を登録し\
    → callback が書いてあるファイルを import
    して「配線情報」を読み込ませる

あなたの構成だと：

-   **sales_overview.py**：単一ドロップダウン + グラフ + コールバック\
-   **sales_by_category_region.py**：２ドロップダウン + グラフ +
    コールバック\
-   **layout.py**：ページにセクションを並べる\
-   **app.py**：serve_layout を登録 & callback を持つファイルを import

------------------------------------------------------------------------

## 1. 各ファイル内での「コールバックの連携」

### sales_overview.py の例

``` python
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")
df = pd.read_csv(DATA_PATH)

def layout():
    return html.Div(
        [
            html.H2("カテゴリ別 売上"),

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

            dcc.Graph(
                id="bar-sales",
                figure=px.bar(
                    df,
                    x="product",
                    y="sales",
                    title="製品別売上（全カテゴリ）",
                ),
            ),
        ]
    )

@callback(
    Output("bar-sales", "figure"),
    Input("category-dropdown", "value")
)
def update_sales_overview(selected_category):
    ...
    return fig
```

### layout() 内の部品

  部品           id                  重要プロパティ
  -------------- ------------------- ----------------
  dcc.Dropdown   category-dropdown   value
  dcc.Graph      bar-sales           figure

### callback が行うこと

-   Input("category-dropdown", "value")\
-   Output("bar-sales", "figure")

→ Dropdown の値が変われば関数が呼ばれ、return fig が bar-sales
に反映される

------------------------------------------------------------------------

## 2. 複数 Input（2ドロップダウン）の例

``` python
@callback(
    Output("dual-sales-graph", "figure"),
    Input("dual-category-dropdown", "value"),
    Input("dual-region-dropdown", "value"),
)
def update_dual_sales_graph(selected_category, selected_region):
    ...
    return fig
```

### Input と関数引数の対応

-   dual-category-dropdown.value → selected_category\
-   dual-region-dropdown.value → selected_region\
-   return fig → dual-sales-graph.figure

------------------------------------------------------------------------

## 3. 「ファイル間」の連携

### 3-1. layout.py からセクションを並べる

``` python
from dash import html
from .sales_overview import layout as sales_overview_layout
from .sales_by_category_region import layout as dual_filter_layout

def serve_layout():
    return html.Div(
        [
            html.H1("食品販売ダッシュボード"),
            sales_overview_layout(),
            dual_filter_layout(),
        ],
        style={"margin": "30px"},
    )
```

### 3-2. app.py で callback を有効化

``` python
from dash import Dash
from dashboards.layout import serve_layout

import dashboards.sales_overview
import dashboards.sales_by_category_region

app = Dash(__name__)
app.layout = serve_layout

if __name__ == "__main__":
    app.run(debug=True)
```

重要：\
**import した瞬間に @callback が実行され、Dash に Input/Output
の配線が登録される**

------------------------------------------------------------------------

## 4. request の「一連の流れ」

### サーバ起動時

1.  layout.py が読み込まれ serve_layout が定義\
2.  sales_overview.py の callback が登録\
3.  sales_by_category_region.py の callback も登録\
4.  準備完了

------------------------------------------------------------------------

### 初回アクセス

1.  Dash が serve_layout() を実行\
2.  sales_overview_layout(), dual_filter_layout()
    が実行され、部品を生成\
3.  コンポーネントツリーを JSON 化してブラウザへ送信\
4.  ブラウザが描画

------------------------------------------------------------------------

### ユーザー操作（例："Fruits" を選択）

1.  category-dropdown.value が更新され JSON がサーバに送信\
2.  Dash が該当 callback を特定\
3.  update_sales_overview("Fruits") を実行\
4.  return fig → bar-sales.figure にセット\
5.  ブラウザ側の Graph が更新される

------------------------------------------------------------------------

## 5. まとめ

-   layout()：コンポーネントを id つきで作る\
-   callback：id と prop を使って "配線" を書く\
-   layout.py：セクションを並べるだけ\
-   app.py：callback を持つファイルを import するだけ\
-   Input(id, prop) → 関数引数\
-   Output(id, prop) ← return fig

------------------------------------------------------------------------
