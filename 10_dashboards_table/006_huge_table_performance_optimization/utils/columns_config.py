# utils/columns_config.py

# Dash DataTable 用の段付きヘッダー定義
#   name: [上段, 中段, 下段]
#   id  : DataFrame の列名と一致させる

COLUMNS = [
    # --- Meta ---
    {"name": ["Meta", "", "ID"], "id": "id"},
    {"name": ["Meta", "", "Date"], "id": "date"},
]

# --- Products (product_1〜product_9) ---  ←★ ここが 14 → 9 列に変更
for i in range(1, 10):  # 1〜9
    COLUMNS.append(
        {
            "name": ["Products", "", f"product_{i}"],
            "id": f"product_{i}",
        }
    )

# --- Nominal Categories (category_1〜category_5) --- ←★ 新規追加
for i in range(1, 6):  # 1〜5
    COLUMNS.append(
        {
            "name": ["Nominal", "", f"category_{i}"],
            "id": f"category_{i}",
        }
    )

# --- Quantities (quantity_1〜quantity_6) ---
for i in range(1, 7):
    COLUMNS.append(
        {
            "name": ["Quantities", "", f"quantity_{i}"],
            "id": f"quantity_{i}",
        }
    )

# --- Mixed (mixed_1〜mixed_29) ---
for i in range(1, 29):
    COLUMNS.append(
        {
            "name": ["Mixed", "", f"mixed_{i}"],
            "id": f"mixed_{i}",
        }
    )
