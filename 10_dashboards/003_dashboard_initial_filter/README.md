# Dash グローバルフィルタ構成の全体フロー（README 用）

## 0. ディレクトリ構成（前提）

```
001_simple_dashboard/
├─ app.py
├─ dashboards/
│   ├─ __init__.py
│   ├─ layout.py                    ← ページ全体の骨組み
│   ├─ filters.py                   ← グローバルフィルタ + filtered-data
│   ├─ sales_overview.py            ← グラフ①（カテゴリ別）
│   └─ sales_by_category_region.py  ← グラフ②（カテゴリ×地域）
└─ data/
    └─ sales.csv
```

**ポイント：**

- データの入り口は **filters.py の df_raw** だけ
- そこからフィルタ処理 → `dcc.Store(id="filtered-data")` に格納
- 各グラフはすべてこの filtered-data を参照

---

## 1. 起動時〜初回表示までの流れ

### 1-1. app.py の役割

```python
from dash import Dash
from dashboards.layout import serve_layout

import dashboards.filters
import dashboards.sales_overview
import dashboards.sales_by_category_region

app = Dash(__name__)
app.layout = serve_layout

if __name__ == "__main__":
    app.run(debug=True)
```

### app.py がやっていることは 3つだけ：

1. `serve_layout`（ページ全体のレイアウト関数）を読み込む  
2. `filters / sales_overview / sales_by_category_region` を **import するだけ**で  
   → それぞれの @callback が Dash に登録される（副作用）  
3. `app.layout = serve_layout` で「この関数が画面を作る」と指定

**重要：app.py は callback を直接呼ばない。import するだけ。  
@callback デコレータが Dash に配線を登録する。**

---

## 1-2. layout.py でページの骨組みを作る

```python
from dash import html

from .filters import layout as filters_layout
from .sales_overview import layout as sales_overview_layout
from .sales_by_category_region import layout as dual_filter_layout

def serve_layout():
    return html.Div(
        [
            html.H1("食品販売ダッシュボード"),

            filters_layout(),        # グローバルフィルタ + dcc.Store(filtered-data)
            sales_overview_layout(), # グラフ① セクション
            dual_filter_layout(),    # グラフ② セクション
        ],
        style={"margin": "30px"},
    )
```

この serve_layout() が返す構造：

- filters セクション
- グラフ①
- グラフ②  
を子要素として持つ **レイアウトツリー（大きな html.Div）**

Dash はこのツリーを JSON 化してブラウザに送信し、  
ブラウザ側の Dash/React が HTML として描画する。

---

## 2. グローバルフィルタで起きていること（filters.py）

### 2-1. データの唯一の入り口

```python
df_raw = pd.read_csv(DATA_PATH)
df_raw["purchase_date"] = pd.to_datetime(df_raw["purchase_date"])
df_raw["sales_date"] = pd.to_datetime(df_raw["sales_date"])
```

df_raw は **全データの唯一の入り口**

---

### 2-2. フィルタ UI と dcc.Store(filtered-data)

```python
def layout():
    return html.Div(
        [
            ...  # 各種スライダーやドロップダウン

            dcc.Store(id="filtered-data"),  # ★ 全グラフ共通のデータ置き場
        ]
    )
```

`dcc.Store(id="filtered-data")` は  
**グローバルフィルタの結果を全グラフに渡す“共有メモリ”**。

---

### 2-3. フィルタ処理コールバック

```python
@callback(
    Output("filtered-data", "data"),
    Input("filter-purchase-date-slider", "value"),
    Input("filter-sales-date-slider", "value"),
    Input("filter-quantity-slider", "value"),
    Input("filter-company-dropdown", "value"),
)
def update_filtered_data(purchase_range, sales_range, qty_range, company):
    df = df_raw.copy()
    df = df[
        (df["purchase_date"] >= p_start_date)
        & (df["purchase_date"] <= p_end_date)
        & (df["sales_date"]    >= s_start_date)
        & (df["sales_date"]    <= s_end_date)
        & (df["quantity"]      >= min_q)
        & (df["quantity"]      <= max_q)
    ]
    if company:
        df = df[df["company"] == company]

    return df.to_dict("records")
```

### 処理の流れ

1. ユーザーがフィルタ UI を操作  
2. df_raw を条件で絞る  
3. DataFrame → JSON(dict list) に変換  
4. `dcc.Store(id="filtered-data").data` に保存  
5. 全グラフがこの値を Input として受け取る

---

## 3. 各グラフセクション側の連携（横のつながり）

**全グラフの共通ルール：**

- Input("filtered-data", "data") を受け取ってから図を作る  
- dcc.Store の中身（JSON）を DataFrame に戻して利用する

---

## 3. 各グラフセクション側の連携  
ここからは **横のつながり**（filters → 各グラフ）の説明です。

---

## 3-1. グラフ①：`sales_overview.py`（カテゴリ別）

### ● レイアウト側

```python
def layout():
    return html.Div(
        [
            html.H2("カテゴリ別 売上（グローバルフィルタ適用）"),

            dcc.Dropdown(
                id="category-dropdown",
                options=[],      # options は callback で更新
                value=None,
                clearable=True,
                placeholder="カテゴリを選択（未選択なら全カテゴリ）",
            ),

            dcc.Graph(id="bar-sales"),
        ]
    )
```

---

### ● コールバック側

```python
@callback(
    Output("bar-sales", "figure"),
    Output("category-dropdown", "options"),
    Output("category-dropdown", "value"),
    Input("filtered-data", "data"),      # ★ グローバルフィルタ結果
    Input("category-dropdown", "value"), # ローカルカテゴリ選択
)
def update_sales_overview(filtered_records, selected_category):
    ...
```

---

### ● ここでの連携

| Input | 内容 | 渡される値 |
|-------|-------|------------|
| **("filtered-data", "data")** | グローバルフィルタ済みの JSON | filtered_records |
| **("category-dropdown", "value")** | セクション内カテゴリ選択 | selected_category |

Output は以下：

- **("bar-sales", "figure")**  
- **("category-dropdown", "options")**  
- **("category-dropdown", "value")**  

→ グローバルフィルタ + ローカルカテゴリ選択 を使って  
カテゴリ別グラフを更新する。

---

## 3-2. グラフ②：`sales_by_category_region.py`（カテゴリ×地域 + 軸選択）

### ● レイアウト側

```python
def layout():
    return html.Div(
        [
            html.H2("カテゴリ × 地域 別 売上（グローバルフィルタ適用）"),

            dcc.Dropdown(id="dual-category-dropdown", ...),
            dcc.Dropdown(id="dual-region-dropdown", ...),

            # 横軸（日付）選択
            dcc.Dropdown(
                id="axis-date-dropdown",
                options=[
                    {"label": "購入日 (purchase_date)", "value": "purchase_date"},
                    {"label": "販売日 (sales_date)", "value": "sales_date"},
                ],
                value="sales_date",
            ),

            # 縦軸（数値）選択
            dcc.Dropdown(
                id="axis-metric-dropdown",
                options=[
                    {"label": "売上 (sales)", "value": "sales"},
                    {"label": "数量 (quantity)", "value": "quantity"},
                ],
                value="sales",
            ),

            dcc.Graph(id="dual-sales-graph"),
        ]
    )
```

---

### ● コールバック側

```python
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
    ...
```

---

### ● ここでの連携（Input）

| Input | 役割 |
|-------|-------|
| **filtered-data.data** | 全グラフ共通のフィルタ済みデータ |
| **dual-category-dropdown.value** | 追加のカテゴリ絞り込み |
| **dual-region-dropdown.value** | 地域の絞り込み |
| **axis-date-dropdown.value** | 横軸の日時列 |
| **axis-metric-dropdown.value** | 縦軸の数値列 |

この情報をもとに：

- df をさらにカテゴリ × 地域で絞り
- 横軸（購入日 or 販売日）
- 縦軸（売上 or 数量）

を選んでグラフを描画する。

---

## 4. ユーザー操作ごとの「再計算の流れ」

### 4-1. グローバルフィルタを触った場合

ユーザーが以下を変更：

- 購入日スライダー  
- 販売日スライダー  
- 数量スライダー  
- 会社ドロップダウン  

**すると：**

1. `update_filtered_data(...)`（filters.py）が実行  
2. `filtered-data.data` が新しい値に更新  
3. それを Input に持つすべてのコールバックが再実行

→ 再実行される：

- update_sales_overview(...)
- update_dual_sales_graph(...)

**→ 全グラフが一斉に更新される**

---

### 4-2. グラフ内のローカルフィルタを触った場合

例：グラフ②のカテゴリを変更したとき

- dual-category-dropdown.value が更新  
- update_dual_sales_graph(...) だけが再実行  

**→ グラフ②だけ更新  
→ グラフ①は Input に影響しないので動かない**

---

## 5. まとめ（ワンフレーズで言うと）

### filters.py
- CSV を **1回だけ**読み込む  
- グローバルフィルタで df_raw を絞る  
- 結果を `dcc.Store("filtered-data")` に保存（JSON）

### sales_overview.py / sales_by_category_region.py
- **必ず filtered-data.data を Input** に持つ  
- そこからローカルフィルタ（カテゴリ, 地域, 横軸, 縦軸）を適用  
- グラフやドロップダウンの options/value を更新

### layout.py
- filters / グラフ① / グラフ② をページに並べるだけ

### app.py
- layout を登録し  
- callback を持つファイルを **import するだけで配線が有効化**

---

この章は、グローバルフィルタと各グラフセクションが  
どのようにデータを受け取り、どう再描画されるかを  
完全に理解するための整理になっています。
