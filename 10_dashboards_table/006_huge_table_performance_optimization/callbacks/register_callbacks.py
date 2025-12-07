# callbacks/register_callbacks.py
from callbacks.filters.product1_filter_callbacks import (
    register_product1_filter,
    register_product1_combined,
)
from callbacks.apply_filters import register_apply_filters
from callbacks.collapse_callbacks import register_collapse_callbacks

def register_all_callbacks(app):    

    # product_1 フィルター
    register_product1_filter(app)
    register_product1_combined(app)

    # テーブルにフィルターを反映
    register_apply_filters(app)

    # サイドバー内の折りたたみ
    register_collapse_callbacks(app)

    # 今後フィルターを増やしたら、ここに register_xxx(app) を追加
