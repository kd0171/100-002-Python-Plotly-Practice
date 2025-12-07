from dash import Input, Output, callback
import pandas as pd
import plotly.express as px
import os

# layout.py と同じように絶対パスを作る
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales.csv")

df = pd.read_csv(DATA_PATH)
@callback(
    Output("bar-sales", "figure"),
    Input("category-dropdown", "value")
)
def update_sales_graph(selected_category):
    filtered = df[df["category"] == selected_category]
    fig = px.bar(
        filtered,
        x="product",
        y="sales",
        title=f"{selected_category} の製品別売上"
    )
    return fig
