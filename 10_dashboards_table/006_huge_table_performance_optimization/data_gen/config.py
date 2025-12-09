# config.py
import datetime as dt

# 0列目：ID（ユニーク）
ID_COLUMN = {
    "name": "id",
    "type": "id_unique",   # 独自タイプ
    "letters_min": 2,
    "letters_max": 4,
    "digits_min": 4,
    "digits_max": 6,
    # null_prob は付けない＝必ず値あり
}

# 1列目：ランダム日付
DATE_COLUMN = {
    "name": "date",
    "type": "date_random",
    "start": dt.date(2010, 1, 1),    # 日付の下限（自由に変えてOK）
    "end": dt.date(2025, 12, 31),    # 日付の上限
    "format": "%Y-%m-%d",            # 出力フォーマット
}

# 2〜9列目：ランダム文字列（商品系） => 8列に縮小
# ---------------------------------------------
# 旧:
# STRING_COLUMNS = [
#     {
#         "name": f"product_{i}",
#         "type": "string_random",
#         ...
#     }
#     for i in range(1, 10)            # 2〜10列 => 9列
# ]
STRING_COLUMNS = [
    {
        "name": f"product_{i}",
        "type": "string_random",
        "length": 12,
        "null_prob": 0.1,
    }
    for i in range(1, 9)              # 1〜8 だけ product にする
]

# ★ 新規：レビュー用の列（短いテキスト）
REVIEW_COLUMN = {
    "name": "review",
    "type": "nominal",   # 既存の nominal ロジックを流用
    # ここに 5〜6語以内のフレーズをいくつか用意しておく
    "choices": [
        "high performance in cold weather",
        "frequent minor failures reported",
        "stable but needs maintenance",
        "excellent fuel efficiency overall",
        "no major issues so far",
        "hard to install and configure",
        "good value for daily usage",
        "requires frequent software updates",
        "noise level higher than expected",
        "great support from vendor team",
        # …必要に応じて増やす
    ],
    "null_prob": 0.0,
}

# 11〜15列目：名義尺度（カテゴリ列） => 5列追加
# choices は好きなカテゴリに変更してください
NOMINAL_COLUMNS = [
    {
        "name": f"category_{i}",
        "type": "nominal",
        "choices": ["A", "B", "C", "D"],  # 名義尺度のカテゴリ
        "null_prob": 0.1,
    }
    for i in range(1, 6)             # 11〜15列 => 5列
]

# 16〜21列目：数量指数（小数・レンジ違い）
QUANTITY_COLUMNS = [
    {
        "name": f"quantity_{i}",
        "type": "float_range",
        "min": min_v,
        "max": max_v,
        "decimals": 2,               # 小数点以下桁数
        "null_prob": 0.1,
    }
    for i, (min_v, max_v) in enumerate([
        (0.0, 1.0),
        (1.0, 10.0),
        (10.0, 100.0),
        (100.0, 1000.0),
        (1000.0, 10000.0),
        (10000.0, 100000.0),
    ], start=1)
]

# 22〜50列目：数値 or 文字列のミックス
MIXED_COLUMNS = [
    {
        "name": f"mixed_{i}",
        "type": "mixed",
        "float_range": (0.0, 1000.0),
        "decimals": 2,
        "string_length": 8,
        "prob_float": 0.5,          # 数値を出す確率（残りは文字列）
        "null_prob": 0.1,
    }
    for i in range(1, 29)           # 22〜50列 => 29列
]

# 全列まとめ
COLUMN_DEFINITIONS = (
    [ID_COLUMN] +
    [DATE_COLUMN] +
    STRING_COLUMNS +
    [REVIEW_COLUMN] +  # ★ product_8 の後ろに review を挿入
    NOMINAL_COLUMNS +
    QUANTITY_COLUMNS +
    MIXED_COLUMNS
)