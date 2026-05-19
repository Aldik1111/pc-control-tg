import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from data.logger import log_action, get_log, get_user_log, log_generator, get_last_logs

TEST_LOG = "data/log.json"


class TestLogger(unittest.TestCase):

    def setUp(self):
        with open(TEST_LOG, "w") as f:
            json.dump([], f)

    def tearDown(self):
        with open(TEST_LOG, "w") as f:
            json.dump([], f)

    # ─── Существующие тесты ───────────────────────────────────

    def test_log_action_adds_entry(self):
        log_action(111, "Screenshot")
        self.assertEqual(len(get_log()), 1)

    def test_log_action_saves_correct_data(self):
        log_action(222, "Open VS Code")
        entry = get_log()[0]
        self.assertEqual(entry["user_id"], 222)
        self.assertEqual(entry["action"], "Open VS Code")

    def test_multiple_actions(self):
        log_action(333, "Screenshot")
        log_action(333, "Open Discord")
        log_action(444, "Webcam photo")
        self.assertEqual(len(get_log()), 3)

    def test_get_user_log_filters_correctly(self):
        log_action(555, "Screenshot")
        log_action(666, "Open Telegram")
        log_action(555, "Webcam photo")
        user_entries = get_user_log(555)
        self.assertEqual(len(user_entries), 2)
        for entry in user_entries:
            self.assertEqual(entry["user_id"], 555)

    def test_empty_log_returns_empty_list(self):
        self.assertEqual(get_log(), [])

    # ─── Тесты генератора ─────────────────────────────────────

    def test_log_generator_is_generator(self):
        import types
        gen = log_generator(5)
        self.assertIsInstance(gen, types.GeneratorType)

    def test_log_generator_yields_correct_count(self):
        for i in range(5):
            log_action(100, f"Action {i}")
        result = list(log_generator(3))
        self.assertEqual(len(result), 3)

    def test_log_generator_yields_last_entries(self):
        log_action(100, "First")
        log_action(100, "Second")
        log_action(100, "Third")
        result = list(log_generator(2))
        actions = [e["action"] for e in result]
        self.assertIn("Third", actions)
        self.assertIn("Second", actions)
        self.assertNotIn("First", actions)

    def test_log_generator_empty_log(self):
        result = list(log_generator(5))
        self.assertEqual(result, [])

    def test_log_generator_n_larger_than_log(self):
        log_action(100, "A")
        log_action(100, "B")
        log_action(100, "C")
        result = list(log_generator(10))
        self.assertEqual(len(result), 3)

    # ─── Тест get_last_logs ───────────────────────────────────

    def test_get_last_logs_empty(self):
        result = get_last_logs(5)
        self.assertIn("No history", result)

    def test_get_last_logs_contains_action(self):
        log_action(123, "WeatherCheck")
        result = get_last_logs(5)
        self.assertIn("WeatherCheck", result)


if __name__ == "__main__":
    unittest.main()