# utils/columns_config.py

# Dash DataTable 用の段付きヘッダー定義
#   name: [上段, 中段, 下段]
#   id  : DataFrame の列名と一致させる
COLUMNS = [
    {"name": ["Meta", "", "id"],   "id": "id"},
    {"name": ["Meta", "", "date"], "id": "date"},
]

# Products: product_1〜product_8
for i in range(1, 9):
    COLUMNS.append(
        {"name": ["Products", "", f"product_{i}"], "id": f"product_{i}"}
    )

# ★ Products グループの中に review 列を追加
COLUMNS.append(
    {"name": ["Products", "", "review"], "id": "review"}
)

# Nominal
for i in range(1, 6):
    COLUMNS.append(
        {"name": ["Nominal", "", f"category_{i}"], "id": f"category_{i}"}
    )

# Quantities
for i in range(1, 7):
    COLUMNS.append(
        {"name": ["Quantities", "", f"quantity_{i}"], "id": f"quantity_{i}"}
    )

# Mixed
for i in range(1, 29):
    COLUMNS.append(
        {"name": ["Mixed", "", f"mixed_{i}"], "id": f"mixed_{i}"}
    )

# Review グループを作る案もあり
COLUMNS.append(
    {"name": ["Review", "", "review"], "id": "review"}
)
COLUMNS.append(
    {"name": ["Review", "", "review_cluster"], "id": "review_cluster"}
)
