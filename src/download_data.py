from pathlib import Path
from urllib.request import urlretrieve

DATA_URL = "https://raw.githubusercontent.com/imvinay0/Zepto-MY-SQL-Data-Analysis-Project/main/zepto.csv"
ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "zepto_inventory_raw.csv"


def main() -> None:
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    if RAW_PATH.exists():
        print(f"Dataset already exists: {RAW_PATH}")
        return
    urlretrieve(DATA_URL, RAW_PATH)
    print(f"Downloaded dataset to: {RAW_PATH}")


if __name__ == "__main__":
    main()
