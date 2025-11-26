# Dash における「サイドバー開閉 × DataTable 自動リサイズ」設計ガイド

Dash では、サイドバーを開閉した際に **DataTable が自動的に縮む／広がるレイアウト** を実現できます。  
ポイントは次の 2 つです。

- **レイアウトの幅管理は CSS（flex あるいは Bootstrap Grid）で行う**
- **サイドバーの開閉状態はコールバックで切り替える**

これにより、サイドバーの表示幅が変化した分だけ、中央のコンテンツ（DataTable）が自然にリサイズされます。

---

## 1. Flex レイアウトを使った最もシンプルな構成

Bootstrap を使わない場合でも、`display: flex` を利用すれば簡潔に実装できます。

```
import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame({
    "A": range(10),
    "B": [x**2 for x in range(10)]
})

app.layout = html.Div(
    [
        # サイドバーの開閉ボタン
        html.Button(
            "フィルタを開閉",
            id="toggle-sidebar",
            n_clicks=0,
            style={"margin": "8px"}
        ),

        # メイン部分全体（flexコンテナ）
        html.Div(
            id="main-area",
            style={
                "display": "flex",
                "height": "80vh",   # 必要に応じて調整
            },
            children=[
                # サイドバー
                html.Div(
                    id="sidebar",
                    style={
                        "width": "250px",          # 開いているときの幅
                        "transition": "width 0.3s",
                        "overflow": "hidden",      # 幅を0にしても中身がはみ出ない
                        "border-right": "1px solid #ccc",
                        "padding": "8px",
                        "boxSizing": "border-box",
                    },
                    children=[
                        html.H4("フィルタ"),
                        # ここに各種フィルターを置く（Dropdown, Checklist など）
                        dcc.Checklist(
                            options=[{"label": f"opt {i}", "value": i} for i in range(5)],
                            value=[],
                            id="dummy-filter"
                        ),
                    ],
                ),

                # テーブル領域（flex: 1 で残り全部を占有）
                html.Div(
                    id="table-area",
                    style={
                        "flex": "1",
                        "minWidth": 0,     # これがないと横スクロールが変になることがある
                        "padding": "8px",
                        "boxSizing": "border-box",
                    },
                    children=[
                        dash_table.DataTable(
                            id="table",
                            data=df.to_dict("records"),
                            columns=[{"name": c, "id": c} for c in df.columns],
                            page_size=10,
                            style_table={
                                "height": "100%",
                                "width": "100%",
                                "overflowX": "auto",
                            },
                        )
                    ],
                ),
            ]
        )
    ]
)

```

この構成では以下が実現されます。

- サイドバーの幅が `250px → 0px` にアニメーションしながら縮む  
- 残りのスペースは `flex: 1` が与えられた **DataTable 領域が自動で埋める**

親コンテナで DataTable の幅を決めていても、  
**「サイドバー + メイン領域」を flex で並べる構造に変更するだけ**で、この挙動に対応できます。

---

## 2. サイドバー開閉のコールバック

```
@app.callback(
    Output("sidebar", "style"),
    Input("toggle-sidebar", "n_clicks"),
    State("sidebar", "style"),
)
def toggle_sidebar(n_clicks, current_style):
    # 初回は何もしない
    if n_clicks is None:
        return current_style

    style = current_style.copy()

    # 偶数クリック → 閉じる、奇数クリック → 開く、という簡単なトグル
    if n_clicks % 2 == 1:
        # 開く
        style["width"] = "250px"
    else:
        # 閉じる
        style["width"] = "0px"

    return style

```

コールバックでは、サイドバーの `width` や `display` をトグルし、  
それに応じてメイン領域（DataTable 側）が自動でリサイズされるようにします。

---

## 3. dash_bootstrap_components を使う場合

Bootstrap を利用している場合は、`dbc.Row` / `dbc.Col` によってレイアウトを構成できます。

- `dbc.Row` の中に  
  - サイドバー列  
  - メインテーブル列  
  の 2 つの `dbc.Col` を配置する
- コールバックで **Col の width（例：`col-3` / `col-9`）や `style` をトグル**する

Bootstrap Grid を切り替える方法でも構築できますが、  
レイアウト制御の簡潔さを優先するなら **flex + width を切り替える方がシンプル**です。

---

## 4. Bootstrap を使う場合のレイアウト例のイメージ

```
import dash
from dash import html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# ダミーデータ
df = pd.DataFrame({
    "A": range(10),
    "B": [x**2 for x in range(10)]
})

# サイドバーのデフォルト style（再利用しやすいように変数に）
SIDEBAR_BASE_STYLE = {
    "height": "80vh",
    "borderRight": "1px solid #ccc",
    "padding": "8px",
    "boxSizing": "border-box",
    "overflowY": "auto",
}

app.layout = dbc.Container(
    fluid=True,
    children=[
        # トグルボタン
        dbc.Button(
            "フィルタを開閉",
            id="toggle-sidebar",
            n_clicks=0,
            className="my-2"
        ),

        # メインエリア
        dbc.Row(
            id="main-row",
            children=[
                # サイドバー列
                dbc.Col(
                    id="sidebar-col",
                    width=3,   # 開いている時は col-3
                    children=[
                        html.H4("フィルタ"),
                        dcc.Checklist(
                            options=[{"label": f"opt {i}", "value": i} for i in range(5)],
                            value=[],
                            id="dummy-filter"
                        ),
                    ],
                    style=SIDEBAR_BASE_STYLE,
                ),

                # テーブル列
                dbc.Col(
                    id="table-col",
                    width=9,  # 残りの幅
                    children=[
                        dash_table.DataTable(
                            id="table",
                            data=df.to_dict("records"),
                            columns=[{"name": c, "id": c} for c in df.columns],
                            page_size=10,
                            style_table={
                                "height": "80vh",
                                "width": "100%",
                                "overflowX": "auto",
                            },
                        )
                    ],
                ),
            ]
        )
    ]
)

# サイドバー開閉コールバック
@app.callback(
    Output("sidebar-col", "style"),
    Output("table-col", "width"),
    Input("toggle-sidebar", "n_clicks"),
    State("sidebar-col", "style"),
)
def toggle_sidebar(n_clicks, current_style):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    # 初回 style をベースにコピー
    style = (current_style or {}).copy()

    # 奇数クリック → サイドバー開、偶数クリック → 閉
    if n_clicks % 2 == 1:
        # 開く：サイドバー表示、テーブルは 9 列
        for k, v in SIDEBAR_BASE_STYLE.items():
            style[k] = v
        # display を戻す
        style.pop("display", None)
        table_width = 9
    else:
        # 閉じる：サイドバーを非表示、テーブルは 12 列
        style["display"] = "none"
        table_width = 12

    return style, table_width


if __name__ == "__main__":
    app.run_server(debug=True)

```

- **サイドバー開時**  
  - サイドバー：`width=3`  
  - テーブル：`width=9`  
- **サイドバー閉時**  
  - サイドバー：`display: none`  
  - テーブル：`width=12`

DataTable 側は単に `style_table={"width": "100%"}` にしておけば、  
親カラムのサイズに合わせて **自動で縮んだり広がったり** します。

---

## まとめ

- **「サイドバーの幅をトグル」＋「メイン領域を flex:1（または Bootstrap Col）」**  
  だけで、サイドバー開閉に応じた自動リサイズレイアウトが完成します。

- DataTable 自体を固定幅にする必要はなく、  
  **親コンテナの幅に対して `width:100%` で表示すれば十分対応可能** です。

- Bootstrap を利用している場合は、`dbc.Col` の幅調整（あるいは `display:none`）を  
  コールバックで切り替える構造が最も扱いやすいです。

