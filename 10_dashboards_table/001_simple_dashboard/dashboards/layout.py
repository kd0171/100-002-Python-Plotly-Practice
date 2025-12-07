from dash import html
from .components.sales_summary import create_sales_bar
from .components.controls import category_dropdown
import pandas as pd
import os

# パスが「実行ディレクトリから見て存在しない」 
# df = pd.read_csv("data/sales.csv")

# 絶対パスに変換:どこで実行しても必ず正しいファイルが読める（最も安定・推奨）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")

# ここで1回だけCSVを読む
df = pd.read_csv(DATA_PATH)

def serve_layout():
    return html.Div(
        [
            html.H1("食品販売ダッシュボード"),

            # 🔹 ドロップダウン
            category_dropdown(df["category"].unique()),

            # 🔹 グラフ
            html.Div(
                [
                    create_sales_bar(df),
                ],
                id="graph-container"
            )
        ],
        style={"margin": "30px"}
    )
