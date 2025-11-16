# Dash アプリの構造と Callback のつながり方（README 形式）

ファイルを分け始めた瞬間に「どこでどう繋がっているのか？」が見えなくなる問題を整理した説明です。

Dash の基本的な動作は以下の通りです。

-   **ページに置くすべてのパーツ（Dropdown / Graph）には id がつく**
-   **callbacks.py が "どの id のどのプロパティ → どの id
    のどのプロパティ" を結ぶ「対応表」になる**
-   **Dash はこの対応表にもとづいて、Input
    の値をコールバック関数の引数に自動で渡す**

以下は、あなたの構成をベースにした詳細な流れです。

------------------------------------------------------------------------

## 0. ファイルの役割

    app.py
    dashboards/
      ├ layout.py
      ├ callbacks.py
      └ components/
           ├ controls.py
           └ sales_summary.py

### app.py

``` python
from dash import Dash
from dashboards.layout import serve_layout
import dashboards.callbacks  # ← コールバックを登録するために読み込むだけ

app = Dash(__name__)
app.layout = serve_layout

if __name__ == "__main__":
    app.run(debug=True)
```

ポイント：

-   `app.layout = serve_layout`\
    → ページのレイアウトは serve_layout() が返す内容になる
-   `import dashboards.callbacks`\
    → @callback を「登録」するだけ（この import
    がないとコールバックが動かない）

------------------------------------------------------------------------

## 1. レイアウト（画面の骨組み）がどう作られるか

### layout.py

``` python
from dash import html
from .components.sales_summary import create_sales_bar
from .components.controls import category_dropdown
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")
df = pd.read_csv(DATA_PATH)

def serve_layout():
    return html.Div(
        [
            html.H1("食品販売ダッシュボード"),

            category_dropdown(df["category"].unique()),

            html.Div(
                [
                    create_sales_bar(df),
                ],
                id="graph-container"
            )
        ],
        style={"margin": "30px"}
    )
```

------------------------------------------------------------------------

### controls.py（ドロップダウン）

``` python
from dash import dcc, html

def category_dropdown(options):
    return html.Div([
        html.Label("カテゴリ選択"),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{"label": o, "value": o} for o in options],
            value=options[0],
            clearable=False
        ),
    ])
```

------------------------------------------------------------------------

### sales_summary.py（グラフ）

``` python
import plotly.express as px
from dash import dcc
import pandas as pd

def create_sales_bar(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="product",
        y="sales",
        title="製品別売上"
    )
    return dcc.Graph(id="bar-sales", figure=fig)
```

------------------------------------------------------------------------

## 2. コールバック（どことどこが連動するか）

``` python
from dash import Input, Output, callback
import pandas as pd
import os
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")
df = pd.read_csv(DATA_PATH)

@callback(
    Output("bar-sales", "figure"),
    Input("category-dropdown", "value")
)
def update_sales_graph(selected_category):

    if selected_category:
        filtered = df[df["category"] == selected_category]
    else:
        filtered = df

    fig = px.bar(
        filtered,
        x="product",
        y="sales",
        title=f"{selected_category} の製品別売上" if selected_category else "製品別売上"
    )
    return fig
```

------------------------------------------------------------------------

## 3. 時系列での処理

### サーバ起動時

1.  layout.py が読み込まれ、serve_layout が登録される\
2.  callbacks.py が読み込まれ、@callback が Dash に登録される

### ブラウザアクセス時

-   serve_layout() が実行され、画面構造が生成される\
-   Dropdown / Graph に id が付与され描画される

### ユーザー操作時

-   category-dropdown.value が変化\
-   Dash が callback を呼び出す\
-   bar-sales.figure が更新され、グラフが描き変わる

------------------------------------------------------------------------

## 4. ファイルを分けても繋がる理由

-   Dropdown や Graph の **実体は layout / components**
-   連動ルールは **callbacks.py にすべて書く**
-   **id とプロパティ名だけで結線されている**

------------------------------------------------------------------------

## 5. ID 対応表

    - category-dropdown : dcc.Dropdown（カテゴリ選択）
      - プロパティ：value

    - bar-sales : dcc.Graph（製品別売上グラフ）
      - プロパティ：figure
