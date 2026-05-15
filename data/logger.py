import json
import os
from datetime import datetime

LOG_FILE = "data/log.json"

def _read_log() -> list:
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception as e:
            return []

def _write_log(entries: list):
    with open(LOG_FILE, "w") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def log_action(user_id: int, action:str):
    entries = _read_log()
    entries.append({
        "user_id": user_id,
        "action": action,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    _write_log(entries)

def get_log() -> list:
    entries = _read_log()

def get_user_log(user_id: int) -> list:
    return [entry for entry in _read_log() if entry["user_id"] == user_id]