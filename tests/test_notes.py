import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from data.notes import add_note, get_all_notes, delete_note, _read_notes

NOTES_FILE = "data/notes.json"


class TestNotes(unittest.TestCase):

    def setUp(self):
        with open(NOTES_FILE, "w") as f:
            json.dump([], f)

    def tearDown(self):
        with open(NOTES_FILE, "w") as f:
            json.dump([], f)

    def test_add_note_adds_entry(self):
        add_note(111, "Buy milk")
        notes = _read_notes()
        self.assertEqual(len(notes), 1)

    def test_add_note_saves_correct_text(self):
        add_note(111, "Hello world")
        notes = _read_notes()
        self.assertEqual(notes[0]["text"], "Hello world")

    def test_add_note_saves_correct_user(self):
        add_note(222, "Test note")
        notes = _read_notes()
        self.assertEqual(notes[0]["user_id"], 222)

    def test_add_multiple_notes(self):
        add_note(111, "Note 1")
        add_note(111, "Note 2")
        add_note(111, "Note 3")
        self.assertEqual(len(_read_notes()), 3)

    def test_notes_have_incremental_ids(self):
        add_note(111, "A")
        add_note(111, "B")
        add_note(111, "C")
        notes = _read_notes()
        ids = [n["id"] for n in notes]
        self.assertEqual(ids, [1, 2, 3])

    def test_delete_note_removes_entry(self):
        add_note(111, "Delete me")
        notes = _read_notes()
        note_id = notes[0]["id"]
        result = delete_note(note_id)
        self.assertTrue(result)
        self.assertEqual(len(_read_notes()), 0)

    def test_delete_note_nonexistent(self):
        result = delete_note(999)
        self.assertFalse(result)

    def test_delete_correct_note(self):
        add_note(111, "Keep me")
        add_note(111, "Delete me")
        notes = _read_notes()
        delete_note(notes[1]["id"])
        remaining = _read_notes()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0]["text"], "Keep me")

    def test_get_all_notes_empty(self):
        result = get_all_notes()
        self.assertIn("No notes", result)

    def test_get_all_notes_contains_text(self):
        add_note(111, "My important note")
        result = get_all_notes()
        self.assertIn("My important note", result)


if __name__ == "__main__":
    unittest.main()