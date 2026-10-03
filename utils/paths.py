"""项目路径常量。

统一从这里取路径，避免在测试文件里写死绝对路径。
此前 tests/ 下有 4 处硬编码了 D:/PycharmProject/saucedemo/data/Data.json，
换机器或进 CI 会直接失败。

用法：
    from utils.paths import DATA_FILE
    test_data = DataLoader(DATA_FILE)
"""
from pathlib import Path

# __file__ = <项目根>/utils/paths.py
# parents[0] = utils，parents[1] = 项目根目录
ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"

DATA_FILE = DATA_DIR / "Data.json"
USERS_FILE = DATA_DIR / "Users.json"
PRODUCTS_FILE = DATA_DIR / "Products.json"
