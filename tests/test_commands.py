import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import MagicMock, patch
from commands.photo_command import WebCamCommand, ScreenshotCommand
from commands.program_command import OpenProgramCommand, CloseProgramCommand




def make_mock(chat_id=12345):
    """Создаёт фейковые bot и message для тестов."""
    bot = MagicMock()
    message = MagicMock()
    message.chat.id = chat_id
    return bot, message


class TestWebCamCommand(unittest.TestCase):

    @patch("commands.photo_command.cv2.VideoCapture")
    @patch("commands.photo_command.cv2.imwrite")
    @patch("commands.photo_command.os.path.exists", return_value=True)
    @patch("commands.photo_command.os.remove")
    def test_execute_sends_photo(self, mock_remove, mock_exists, mock_imwrite, mock_cap):
        """WebCamCommand.execute() должен вызвать send_photo."""
        mock_cap.return_value.read.return_value = (True, MagicMock())
        bot, message = make_mock()

        cmd = WebCamCommand(bot, message)
        cmd.send_photo = MagicMock()  # не открываем реальный файл
        cmd._capture = MagicMock()   # не используем реальную камеру
        cmd.execute()

        cmd.send_photo.assert_called_once_with(WebCamCommand.PATH)

    def test_execute_sends_error_on_failure(self):
        """WebCamCommand.execute() должен отправить сообщение об ошибке при исключении."""
        bot, message = make_mock()
        cmd = WebCamCommand(bot, message)
        cmd._capture = MagicMock(side_effect=RuntimeError("нет камеры"))
        cmd.execute()

        bot.send_message.assert_called_once()
        args = bot.send_message.call_args[0]
        self.assertIn("ERROR CAMERA", args[1])


class TestScreenshotCommand(unittest.TestCase):

    def test_execute_sends_error_on_failure(self):
        """ScreenshotCommand.execute() должен отправить ошибку если pyautogui упал."""
        bot, message = make_mock()
        cmd = ScreenshotCommand(bot, message)
        cmd._capture = MagicMock(side_effect=Exception("экран недоступен"))
        cmd.execute()

        # Должно быть два сообщения: "⏳ Скриншот через..." и "❌ Ошибка..."
        self.assertEqual(bot.send_message.call_count, 2)


class TestOpenProgramCommand(unittest.TestCase):

    @patch("commands.program_command.app_open")
    def test_execute_calls_app_open(self, mock_open):
        """OpenProgramCommand должен вызвать app_open с правильным именем."""
        bot, message = make_mock()
        cmd = OpenProgramCommand(bot, message, "VS Code")
        cmd_screenshot = MagicMock()

        with patch("commands.program_command.ScreenshotCommand", return_value=cmd_screenshot):
            cmd.execute()

        mock_open.assert_called_once_with("VS Code", match_closest=False)

    @patch("commands.program_command.app_open", side_effect=Exception("не найдено"))
    def test_execute_sends_error_on_failure(self, mock_open):
        """OpenProgramCommand должен отправить ошибку если программа не найдена."""
        bot, message = make_mock()
        cmd = OpenProgramCommand(bot, message, "НесуществующаяПрога")
        cmd.execute()

        bot.send_message.assert_called()
        args = bot.send_message.call_args[0]
        self.assertIn("failed", args[1])


class TestCloseProgramCommand(unittest.TestCase):

    @patch("commands.program_command.app_close")
    def test_execute_calls_app_close(self, mock_close):
        """CloseProgramCommand должен вызвать app_close с правильным именем."""
        bot, message = make_mock()
        cmd = CloseProgramCommand(bot, message, "Discord")
        cmd_screenshot = MagicMock()

        with patch("commands.program_command.ScreenshotCommand", return_value=cmd_screenshot):
            cmd.execute()

        mock_close.assert_called_once_with("Discord", match_closest=False)


if __name__ == "__main__":
    unittest.main()