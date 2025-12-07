from callbacks.apply_filters import register_apply_filters
from callbacks.filters.product1_filter_callbacks import register_product1_filter
from callbacks.filters.product2_filter_callbacks import register_product2_filter
from callbacks.filters.mixed1_filter_callbacks import register_mixed1_filter
from callbacks.filters.quantity1_filter_callbacks import register_quantity1_filter
from callbacks.filters.date_filter_callbacks import register_date_filter
from callbacks.collapse_callbacks import register_collapse_callbacks


def register_all_callbacks(app):
    register_product1_filter(app)
    register_product2_filter(app)
    register_mixed1_filter(app)

    register_quantity1_filter(app)  # quantity_1 slider
    register_date_filter(app)       # date slider

    register_apply_filters(app)     # テーブル本体（server-side paging + sort）
    register_collapse_callbacks(app)
