# Dash で複数行ヘッダー＋ドロップダウンフィルタ付きテーブルを作る

このドキュメントでは、Plotly Dash の標準コンポーネントだけを使って、

- **Excel のような複数行ヘッダー**
- **各列を複数選択・検索可能なドロップダウンでフィルタ**

を実現する方法を解説します。

構成は以下のとおりです。

1. [全体像](#全体像)
2. [複数行ヘッダーの定義方法](#複数行ヘッダーの定義方法)
3. [ドロップダウンによるフィルタ UI](#ドロップダウンによるフィルタ-ui)
4. [フルサンプルコード](#フルサンプルコード)
5. [応用のヒント](#応用のヒント)

## 全体像

このドキュメントでは、Plotly Dash の標準コンポーネントだけを使って、

- **Excel のような複数行ヘッダー**
- **各列を複数選択・検索可能なドロップダウンでフィルタ**

を実現する方法を解説します。

ここで目指すテーブルのポイントは次のとおりです。

- `dash_table.DataTable` の **multi-level header 機能** を利用し、  
  例として「Sold_Amount → Fruit / Vegetable → Apple など」の 3 段ヘッダーを構成する。
- 列ごとのフィルタリングは、テーブル上部に配置した **`dcc.Dropdown`（`multi=True`, `searchable=True`）** を使って行う。
- `DataTable` 側では `filter_action="native"` を有効にし、  
  「ドロップダウンでの条件絞り込み」と「各列のテキストフィルタ」を併用できるようにする。

以降の章では、

1. 複数行ヘッダーの具体的な定義方法  
2. ドロップダウンによるフィルタ UI の実装  
3. それらを組み合わせたフルサンプルコード  

の順で詳しく説明していきます。

## 複数行ヘッダーの定義方法

`dash_table.DataTable` では、`columns` 引数の各要素に含まれる `name` を **リスト** で指定すると、  
そのリストの要素数に応じて自動的に複数行ヘッダー（multi-level header）が生成されます。

### 基本アイデア

- `columns[i]["name"]` を `"Apple"` のような単一の文字列ではなく、  
  `["Sold_Amount", "Fruit", "Apple"]` のようなリストにする。
- リストの **先頭要素が上位階層**、末尾にいくほど下位階層（実際の列名）になる。
- `merge_duplicate_headers=True` を指定すると、同じラベルが縦方向・横方向に自動的に結合され、  
  Excel の結合セルに近い見た目になる。

### サンプル：3 段構成のヘッダー

```python
from dash import dash_table

table_columns = [
    # 単純な列（上位階層ラベルなし）
    {"name": ["", "", "Contract_Nr"],  "id": "Contract_Nr"},
    {"name": ["", "", "Buyer_name"],   "id": "Buyer_name"},
    {"name": ["", "", "Buyer_Region"], "id": "Buyer_Region"},

    # 上位ラベル：Sold_Amount → 中位ラベル：Fruit / Vegetable → 下位ラベル：品目名
    {"name": ["Sold_Amount", "Fruit",     "Apple"],   "id": "Apple",   "type": "numeric"},
    {"name": ["Sold_Amount", "Fruit",     "Banana"],  "id": "Banana",  "type": "numeric"},
    {"name": ["Sold_Amount", "Fruit",     "Grape"],   "id": "Grape",   "type": "numeric"},
    {"name": ["Sold_Amount", "Vegetable", "Tomato"],  "id": "Tomato",  "type": "numeric"},
    {"name": ["Sold_Amount", "Vegetable", "Potato"],  "id": "Potato",  "type": "numeric"},
    {"name": ["Sold_Amount", "Vegetable", "Carrot"],  "id": "Carrot",  "type": "numeric"},
]

table = dash_table.DataTable(
    id="sales-table",
    columns=table_columns,
    # DataFrame などから生成した行データを渡す:
    # data=df.to_dict("records"),
    merge_duplicate_headers=True,  # 同じラベルを自動的に結合して表示
)
```

この例では、name が 3 要素のリストになっているため、ヘッダーは 3 段になります。

- 1 行目："" / "" / "Sold_Amount"
- 2 行目："" / "" / "Fruit" または "Vegetable"
- 3 行目："Contract_Nr", "Buyer_name", "Apple" など実際の列名

空文字列 "" を入れている列は、上位階層のラベルを持たない列（単独ヘッダー）を意味します。