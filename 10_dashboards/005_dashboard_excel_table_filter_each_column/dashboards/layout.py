# dashboards/layout.py

import os
from typing import List

import pandas as pd
from dash import html, dash_table, dcc, callback, Input, Output

# ========= データ読み込み =========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sample.csv")

df = pd.read_csv(DATA_PATH, sep=";")  # セミコロン区切り

# ========= 列の順番と幅を一元管理 =========
COLUMN_ORDER: List[str] = [
    "Contract_Nr",
    "Buyer_name",
    "Buyer_Region",
    "Apple",
    "Banana",
    "Grape",
    "Tomato",
    "Potato",
    "Carrot",
]

COLUMN_WIDTHS = {
    "Contract_Nr": "110px",
    "Buyer_name": "130px",
    "Buyer_Region": "130px",
    "Apple": "90px",
    "Banana": "90px",
    "Grape": "90px",
    "Tomato": "90px",
    "Potato": "90px",
    "Carrot": "90px",
}

GRID_TEMPLATE = " ".join(COLUMN_WIDTHS[col] for col in COLUMN_ORDER)
TOTAL_WIDTH = sum(int(COLUMN_WIDTHS[col].replace("px", "")) for col in COLUMN_ORDER)

NUMERIC_COLS = ["Apple", "Banana", "Grape", "Tomato", "Potato", "Carrot"]


def serve_layout():
    # --- DataTable の複数行ヘッダー定義 ---
    table_columns = [
        {"name": ["", "", "Contract_Nr"],  "id": "Contract_Nr"},
        {"name": ["", "", "Buyer_name"],   "id": "Buyer_name"},
        {"name": ["", "", "Buyer_Region"], "id": "Buyer_Region"},

        {"name": ["Sold_Amount", "Fruit",     "Apple"],   "id": "Apple"},
        {"name": ["Sold_Amount", "Fruit",     "Banana"],  "id": "Banana"},
        {"name": ["Sold_Amount", "Fruit",     "Grape"],   "id": "Grape"},

        {"name": ["Sold_Amount", "Vegetable", "Tomato"],  "id": "Tomato"},
        {"name": ["Sold_Amount", "Vegetable", "Potato"],  "id": "Potato"},
        {"name": ["Sold_Amount", "Vegetable", "Carrot"],  "id": "Carrot"},
    ]

    style_cell_conditional = [
        {
            "if": {"column_id": col},
            "width": COLUMN_WIDTHS[col],
            "minWidth": COLUMN_WIDTHS[col],
            "maxWidth": COLUMN_WIDTHS[col],
        }
        for col in COLUMN_ORDER
    ]

    # ---------- レイアウト ----------
    return html.Div(
        [
            html.H1("販売データ（連動フィルタ＋列上フィルタ + 固定幅スクロール）"),

            # ▼ この中が横スクロールする（フィルタ行と表を一体で動かす）
            html.Div(
                [
                    # ===== フィルタ行 =====
                    html.Div(
                        [
                            # Contract_Nr: 部分一致テキスト
                            dcc.Input(
                                id="filter-contract",
                                type="text",
                                placeholder="Contract",
                                style={"width": "100%"},
                            ),
                            # Buyer_name: 部分一致テキスト
                            dcc.Input(
                                id="filter-buyer",
                                type="text",
                                placeholder="Buyer",
                                style={"width": "100%"},
                            ),
                            # Buyer_Region: 動的に候補が変わる Dropdown
                            dcc.Dropdown(
                                id="filter-region",
                                options=[],  # 初期はコールバックで埋める
                                value=[],
                                multi=True,
                                searchable=True,
                                placeholder="Region",
                                style={"width": "100%"},
                            ),
                            # 数値列: Apple〜Carrot（候補はコールバックで埋める）
                            dcc.Dropdown(
                                id="filter-Apple",
                                options=[],
                                value=[],
                                multi=True,
                                searchable=True,
                                placeholder="Apple",
                                style={"width": "100%"},
                            ),
                            dcc.Dropdown(
                                id="filter-Banana",
                                options=[],
                                value=[],
                                multi=True,
                                searchable=True,
                                placeholder="Banana",
                                style={"width": "100%"},
                            ),
                            dcc.Dropdown(
                                id="filter-Grape",
                                options=[],
                                value=[],
                                multi=True,
                                searchable=True,
                                placeholder="Grape",
                                style={"width": "100%"},
                            ),
                            dcc.Dropdown(
                                id="filter-Tomato",
                                options=[],
                                value=[],
                                multi=True,
                                searchable=True,
                                placeholder="Tomato",
                                style={"width": "100%"},
                            ),
                            dcc.Dropdown(
                                id="filter-Potato",
                                options=[],
                                value=[],
                                multi=True,
                                searchable=True,
                                placeholder="Potato",
                                style={"width": "100%"},
                            ),
                            dcc.Dropdown(
                                id="filter-Carrot",
                                options=[],
                                value=[],
                                multi=True,
                                searchable=True,
                                placeholder="Carrot",
                                style={"width": "100%"},
                            ),
                        ],
                        id="filter-row",
                        style={
                            "display": "grid",
                            "gridTemplateColumns": GRID_TEMPLATE,
                            "columnGap": "0px",
                            "rowGap": "4px",
                            "minWidth": f"{TOTAL_WIDTH}px",
                            "width": f"{TOTAL_WIDTH}px",
                            "marginBottom": "8px",
                        },
                    ),

                    # ===== DataTable 本体 =====
                    dash_table.DataTable(
                        id="sales-table",
                        columns=table_columns,
                        data=df.to_dict("records"),
                        merge_duplicate_headers=True,
                        sort_action="native",
                        filter_action="none",
                        page_size=20,
                        style_table={
                            "minWidth": f"{TOTAL_WIDTH}px",
                            "width": f"{TOTAL_WIDTH}px",
                        },
                        style_cell={
                            "textAlign": "center",
                            "padding": "0 4px",
                        },
                        style_cell_conditional=style_cell_conditional,
                    ),
                ],
                style={
                    "overflowX": "auto",
                    "border": "1px solid #ccc",
                    "padding": "4px",
                },
            ),
        ],
        style={"margin": "30px"},
    )


# ========= 共通：フィルタ適用関数 =========
def apply_filters(
    base_df: pd.DataFrame,
    contract_text,
    buyer_text,
    region_values,
    apple_values,
    banana_values,
    grape_values,
    tomato_values,
    potato_values,
    carrot_values,
    except_col: str | None = None,
) -> pd.DataFrame:
    """except_col で指定した列以外のフィルタを全部適用した DataFrame を返す"""

    dff = base_df.copy()

    # Contract_Nr（部分一致）
    if except_col != "Contract_Nr" and contract_text:
        s = str(contract_text).lower()
        dff = dff[dff["Contract_Nr"].str.lower().str.contains(s)]

    # Buyer_name（部分一致）
    if except_col != "Buyer_name" and buyer_text:
        s = str(buyer_text).lower()
        dff = dff[dff["Buyer_name"].str.lower().str.contains(s)]

    # Buyer_Region（複数選択）
    if except_col != "Buyer_Region" and region_values:
        dff = dff[dff["Buyer_Region"].isin(region_values)]

    # 数値列（複数選択）
    if except_col != "Apple" and apple_values:
        dff = dff[dff["Apple"].isin(apple_values)]
    if except_col != "Banana" and banana_values:
        dff = dff[dff["Banana"].isin(banana_values)]
    if except_col != "Grape" and grape_values:
        dff = dff[dff["Grape"].isin(grape_values)]
    if except_col != "Tomato" and tomato_values:
        dff = dff[dff["Tomato"].isin(tomato_values)]
    if except_col != "Potato" and potato_values:
        dff = dff[dff["Potato"].isin(potato_values)]
    if except_col != "Carrot" and carrot_values:
        dff = dff[dff["Carrot"].isin(carrot_values)]

    return dff


# ========= メインコールバック：表データ + 各フィルタ候補/値を全部更新 =========
@callback(
    # 1. テーブルのデータ
    Output("sales-table", "data"),
    # 2. Region フィルタの候補と選択値
    Output("filter-region", "options"),
    Output("filter-region", "value"),
    # 3. 数値列フィルタの候補と選択値
    Output("filter-Apple", "options"),
    Output("filter-Apple", "value"),
    Output("filter-Banana", "options"),
    Output("filter-Banana", "value"),
    Output("filter-Grape", "options"),
    Output("filter-Grape", "value"),
    Output("filter-Tomato", "options"),
    Output("filter-Tomato", "value"),
    Output("filter-Potato", "options"),
    Output("filter-Potato", "value"),
    Output("filter-Carrot", "options"),
    Output("filter-Carrot", "value"),
    # ---- Inputs: 全フィルタの現在値 ----
    Input("filter-contract", "value"),
    Input("filter-buyer", "value"),
    Input("filter-region", "value"),
    Input("filter-Apple", "value"),
    Input("filter-Banana", "value"),
    Input("filter-Grape", "value"),
    Input("filter-Tomato", "value"),
    Input("filter-Potato", "value"),
    Input("filter-Carrot", "value"),
)
def update_all_filters_and_table(
    contract_text,
    buyer_text,
    region_values,
    apple_values,
    banana_values,
    grape_values,
    tomato_values,
    potato_values,
    carrot_values,
):
    # None 対策（空リストとして扱う）
    region_values = region_values or []
    apple_values = apple_values or []
    banana_values = banana_values or []
    grape_values = grape_values or []
    tomato_values = tomato_values or []
    potato_values = potato_values or []
    carrot_values = carrot_values or []

    # 1) 全フィルタ適用後のデータ → テーブル用
    dff_all = apply_filters(
        df,
        contract_text,
        buyer_text,
        region_values,
        apple_values,
        banana_values,
        grape_values,
        tomato_values,
        potato_values,
        carrot_values,
        except_col=None,
    )

    # 2) 各フィルタの候補値（自分以外のフィルタだけ適用）
    # Region
    dff_except_region = apply_filters(
        df,
        contract_text,
        buyer_text,
        region_values,  # ★ except_col="Buyer_Region" なのでここは無視される
        apple_values,
        banana_values,
        grape_values,
        tomato_values,
        potato_values,
        carrot_values,
        except_col="Buyer_Region",
    )
    region_candidates = sorted(dff_except_region["Buyer_Region"].unique())
    region_options = [{"label": r, "value": r} for r in region_candidates]
    # 現在の選択値のうち、まだ候補に残っているものだけ維持
    region_values_new = [v for v in region_values if v in region_candidates]

    # Apple
    dff_except_apple = apply_filters(
        df,
        contract_text,
        buyer_text,
        region_values,
        apple_values,
        banana_values,
        grape_values,
        tomato_values,
        potato_values,
        carrot_values,
        except_col="Apple",
    )
    apple_candidates = sorted(dff_except_apple["Apple"].unique())
    apple_options = [{"label": str(v), "value": v} for v in apple_candidates]
    apple_values_new = [v for v in apple_values if v in apple_candidates]

    # Banana
    dff_except_banana = apply_filters(
        df,
        contract_text,
        buyer_text,
        region_values,
        apple_values,
        banana_values,
        grape_values,
        tomato_values,
        potato_values,
        carrot_values,
        except_col="Banana",
    )
    banana_candidates = sorted(dff_except_banana["Banana"].unique())
    banana_options = [{"label": str(v), "value": v} for v in banana_candidates]
    banana_values_new = [v for v in banana_values if v in banana_candidates]

    # Grape
    dff_except_grape = apply_filters(
        df,
        contract_text,
        buyer_text,
        region_values,
        apple_values,
        banana_values,
        grape_values,
        tomato_values,
        potato_values,
        carrot_values,
        except_col="Grape",
    )
    grape_candidates = sorted(dff_except_grape["Grape"].unique())
    grape_options = [{"label": str(v), "value": v} for v in grape_candidates]
    grape_values_new = [v for v in grape_values if v in grape_candidates]

    # Tomato
    dff_except_tomato = apply_filters(
        df,
        contract_text,
        buyer_text,
        region_values,
        apple_values,
        banana_values,
        grape_values,
        tomato_values,
        potato_values,
        carrot_values,
        except_col="Tomato",
    )
    tomato_candidates = sorted(dff_except_tomato["Tomato"].unique())
    tomato_options = [{"label": str(v), "value": v} for v in tomato_candidates]
    tomato_values_new = [v for v in tomato_values if v in tomato_candidates]

    # Potato
    dff_except_potato = apply_filters(
        df,
        contract_text,
        buyer_text,
        region_values,
        apple_values,
        banana_values,
        grape_values,
        tomato_values,
        potato_values,
        carrot_values,
        except_col="Potato",
    )
    potato_candidates = sorted(dff_except_potato["Potato"].unique())
    potato_options = [{"label": str(v), "value": v} for v in potato_candidates]
    potato_values_new = [v for v in potato_values if v in potato_candidates]

    # Carrot
    dff_except_carrot = apply_filters(
        df,
        contract_text,
        buyer_text,
        region_values,
        apple_values,
        banana_values,
        grape_values,
        tomato_values,
        potato_values,
        carrot_values,
        except_col="Carrot",
    )
    carrot_candidates = sorted(dff_except_carrot["Carrot"].unique())
    carrot_options = [{"label": str(v), "value": v} for v in carrot_candidates]
    carrot_values_new = [v for v in carrot_values if v in carrot_candidates]

    # ▼ すべての Output を返す
    return (
        dff_all.to_dict("records"),
        region_options,
        region_values_new,
        apple_options,
        apple_values_new,
        banana_options,
        banana_values_new,
        grape_options,
        grape_values_new,
        tomato_options,
        tomato_values_new,
        potato_options,
        potato_values_new,
        carrot_options,
        carrot_values_new,
    )
