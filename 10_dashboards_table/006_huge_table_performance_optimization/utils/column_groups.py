# utils/column_groups.py

COLUMN_GROUPS = {
    "products": [f"product_{i}" for i in range(1, 9)] + ["review"],
    "review": ["review_cluster"],        # ← 新グループ
    "categories": [f"category_{i}" for i in range(1, 6)],
    "quantities": [f"quantity_{i}" for i in range(1, 7)],
    "mixed": [f"mixed_{i}" for i in range(1, 29)],
}

META_COLUMNS = ["id", "date"]
