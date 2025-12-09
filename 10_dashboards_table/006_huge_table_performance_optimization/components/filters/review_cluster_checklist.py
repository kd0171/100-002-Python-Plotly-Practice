# components/filters/review_cluster_checklist.py
from dash import html, dcc
from components.table_component import test_df


def review_cluster_checklist():
    """
    review_cluster 列を対象にしたチェックリストフィルタ。
    - 上に検索ボックス
    - 下にクラスタ名の一覧
    """

    if "review_cluster" in test_df.columns:
        options = [
            {"label": str(val), "value": str(val)}
            for val in sorted(test_df["review_cluster"].dropna().unique())
        ]
    else:
        options = []

    return html.Div(
        [
            html.Label("Review Cluster", className="form-label"),

            # 検索ボックス
            dcc.Input(
                id="review-cluster-search-box",
                type="text",
                placeholder="Search",
                style={"width": "100%", "marginBottom": "8px"},
            ),

            # チェックリスト
            html.Div(
                dcc.Checklist(
                    id="review-cluster-checklist",
                    options=options,
                    value=[],  # 初期値は未選択
                    inputStyle={"marginRight": "8px"},
                    labelStyle={"display": "block", "marginBottom": "6px"},
                ),
                style={
                    "maxHeight": "180px",
                    "overflowY": "auto",
                    "border": "1px solid #ddd",
                    "borderRadius": "6px",
                    "padding": "6px",
                },
            ),
        ],
        style={"padding": "10px"},
    )
