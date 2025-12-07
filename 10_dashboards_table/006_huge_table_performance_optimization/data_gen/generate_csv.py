# generate_csv.py
import csv
import random
import string
import datetime as dt
from pathlib import Path

from config import COLUMN_DEFINITIONS


# -----------------------------------------
# 出力設定（ユーザーが変える部分）
# -----------------------------------------
OUTPUT_FILENAME = "test_output_20000.csv"
OUTPUT_ROWS = 20000  # 生成したい行数

# -----------------------------------------
# ディレクトリ設定
# -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "database"
DATA_DIR.mkdir(exist_ok=True)  # フォルダがなければ作成

OUTPUT_PATH = DATA_DIR / OUTPUT_FILENAME


# -----------------------------------------
# ランダム生成関数
# -----------------------------------------
def random_date(start: dt.date, end: dt.date) -> dt.date:
    delta_days = (end - start).days
    offset = random.randint(0, delta_days)
    return start + dt.timedelta(days=offset)


def random_string(length: int) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def generate_value(col_def: dict):
    # 欠損値生成（null_prob が設定されていれば）
    null_prob = col_def.get("null_prob", 0.0)
    if null_prob > 0 and random.random() < null_prob:
        return ""  # CSV では空欄が自然

    ctype = col_def["type"]

    if ctype == "date_random":
        d = random_date(col_def["start"], col_def["end"])
        fmt = col_def.get("format", "%Y-%m-%d")
        return d.strftime(fmt)

    elif ctype == "string_random":
        return random_string(col_def.get("length", 10))

    elif ctype == "float_range":
        v = random.uniform(col_def["min"], col_def["max"])
        decimals = col_def.get("decimals", 2)
        return f"{v:.{decimals}f}"

    elif ctype == "mixed":
        if random.random() < col_def.get("prob_float", 0.5):
            min_v, max_v = col_def["float_range"]
            v = random.uniform(min_v, max_v)
            decimals = col_def.get("decimals", 2)
            return f"{v:.{decimals}f}"
        else:
            return random_string(col_def.get("string_length", 8))

    # ★ 名義尺度（カテゴリ）用
    elif ctype == "nominal":
        choices = col_def["choices"]
        return random.choice(choices)

    return ""


def generate_unique_id(col_def: dict, used_ids: set[str]) -> str:
    letters_min = col_def.get("letters_min", 2)
    letters_max = col_def.get("letters_max", 4)
    digits_min = col_def.get("digits_min", 4)
    digits_max = col_def.get("digits_max", 6)

    while True:
        # 文字数をランダムに決定
        n_letters = random.randint(letters_min, letters_max)
        n_digits = random.randint(digits_min, digits_max)

        # アルファベット部分
        letters = "".join(
            random.choice(string.ascii_letters)
            for _ in range(n_letters)
        )
        # 数字部分
        digits = "".join(
            random.choice(string.digits)
            for _ in range(n_digits)
        )

        value = letters + digits

        # 一意性チェック
        if value not in used_ids:
            used_ids.add(value)
            return value


def generate_row(used_ids: set[str]):
    row = []
    for col in COLUMN_DEFINITIONS:
        if col["type"] == "id_unique":
            row.append(generate_unique_id(col, used_ids))
        else:
            row.append(generate_value(col))
    return row


def generate_csv(n_rows: int, filepath: Path):
    used_ids: set[str] = set()

    with filepath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([col["name"] for col in COLUMN_DEFINITIONS])

        for _ in range(n_rows):
            writer.writerow(generate_row(used_ids))

    print(f"\n✔ CSVファイル生成完了: {filepath}")
    print(f"✔ 行数: {n_rows:,}\n")


if __name__ == "__main__":
    generate_csv(OUTPUT_ROWS, OUTPUT_PATH)
