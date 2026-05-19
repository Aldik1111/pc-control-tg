import json
import os
from datetime import datetime

LOG_FILE = "data/log.json"


def _read_log() -> list:
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _write_log(entries: list):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def log_action(user_id: int, action: str):
    entries = _read_log()
    entries.append({
        "user_id": user_id,
        "action": action,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    _write_log(entries)


def log_generator(n: int = 5):
    entries = _read_log()
    for entry in entries[-n:]:
        yield entry


def get_last_logs(n: int = 10) -> str:
    result = "📊 Last actions:\n\n"
    count = 0
    for entry in log_generator(n):
        result += f"🕐 {entry['time']}\n"
        result += f"👤 {entry['user_id']}\n"
        result += f"⚡ {entry['action']}\n"
        result += "─────────────────\n"
        count += 1
    if count == 0:
        return "📭 No history yet."
    return result


def get_log() -> list:
    return _read_log()


def get_user_log(user_id: int) -> list:
    return [entry for entry in _read_log() if entry["user_id"] == user_id]