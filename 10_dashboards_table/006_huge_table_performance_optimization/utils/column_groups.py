# utils/column_groups.py

COLUMN_GROUPS = {
    # "meta": ["id", "date"],  ← 削除

    "products": [f"product_{i}" for i in range(1, 10)],
    "categories": [f"category_{i}" for i in range(1, 6)],
    "quantities": [f"quantity_{i}" for i in range(1, 7)],
    "mixed": [f"mixed_{i}" for i in range(1, 29)],
}

# Meta は別扱いで固定列として常に可視
META_COLUMNS = ["id", "date"]
