import json
import os
from datetime import datetime

NOTES_FILE = "data/notes.json"


def _read_notes() -> list:
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _write_notes(notes: list):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def add_note(user_id: int, text: str):
    """Добавить новую заметку."""
    notes = _read_notes()
    notes.append({
        "id": len(notes) + 1,
        "user_id": user_id,
        "text": text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    _write_notes(notes)


def get_all_notes() -> str:
    """Вернуть все заметки в виде текста."""
    notes = _read_notes()
    if not notes:
        return "📭 No notes yet."
    result = "📝 Notes:\n\n"
    for note in notes:
        result += f"#{note['id']} 🕐 {note['time']}\n"
        result += f"{note['text']}\n"
        result += "─────────────────\n"
    return result


def delete_note(index: int) -> bool:
    """Удалить заметку по номеру. Возвращает True если удалено."""
    notes = _read_notes()
    for i, note in enumerate(notes):
        if note["id"] == index:
            notes.pop(i)
            _write_notes(notes)
            return True
    return False