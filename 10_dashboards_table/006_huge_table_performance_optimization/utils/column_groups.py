# utils/column_groups.py

# 列グループ名 → 対応する列 id のリスト
COLUMN_GROUPS = {
    "meta": [
        "id",
        "date",
    ],
    "products": [
        f"product_{i}" for i in range(1, 10)   # 1〜9
    ],
    "categories": [
        f"category_{i}" for i in range(1, 6)   # 1〜5
    ],
    "quantities": [
        f"quantity_{i}" for i in range(1, 7)   # 1〜6
    ],
    "mixed": [
        f"mixed_{i}" for i in range(1, 29)     # 1〜29
    ],
}
