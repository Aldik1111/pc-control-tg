import unittest
import os
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from commands.logger import log_action, get_log, get_user_log

TEST_LOG = "data/log.json"


class TestLogger(unittest.TestCase):

    def setUp(self):
        """Перед каждым тестом — очищаем лог."""
        with open(TEST_LOG, "w") as f:
            json.dump([], f)

    def tearDown(self):
        """После каждого теста — очищаем лог."""
        with open(TEST_LOG, "w") as f:
            json.dump([], f)

    def test_log_action_adds_entry(self):
        """log_action() должен добавить одну запись в лог."""
        log_action(111, "Screenshot")
        entries = get_log()
        self.assertEqual(len(entries), 1)

    def test_log_action_saves_correct_data(self):
        """Запись должна содержать правильный user_id и action."""
        log_action(222, "Open VS Code")
        entry = get_log()[0]
        self.assertEqual(entry["user_id"], 222)
        self.assertEqual(entry["action"], "Open VS Code")

    def test_multiple_actions(self):
        """Несколько действий должны все сохраниться."""
        log_action(333, "Screenshot")
        log_action(333, "Open Discord")
        log_action(444, "Webcam photo")
        self.assertEqual(len(get_log()), 3)

    def test_get_user_log_filters_correctly(self):
        """get_user_log() должен вернуть только записи нужного пользователя."""
        log_action(555, "Screenshot")
        log_action(666, "Open Telegram")
        log_action(555, "Webcam photo")
        user_entries = get_user_log(555)
        self.assertEqual(len(user_entries), 2)
        for entry in user_entries:
            self.assertEqual(entry["user_id"], 555)

    def test_empty_log_returns_empty_list(self):
        """Пустой лог должен вернуть пустой список."""
        self.assertEqual(get_log(), [])


if __name__ == "__main__":
    unittest.main()