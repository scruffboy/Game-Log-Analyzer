from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = DATA_DIR / "logs"


INVENTORY_LOGS = LOGS_DIR / "inventory_logs.txt"
MONEY_LOGS = LOGS_DIR / "money_logs.txt"
DB_PATH = DATA_DIR / "game_logs.db"


LOGS_DIR.mkdir(parents=True, exist_ok=True)
