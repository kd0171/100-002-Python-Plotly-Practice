import plotly.express as px
from dash import dcc
import pandas as pd

def create_sales_bar(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="category",
        y="sales",
        title="カテゴリ別売上"
    )
    return dcc.Graph(id="bar-sales", figure=fig)
