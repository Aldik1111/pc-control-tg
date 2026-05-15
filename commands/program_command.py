from AppOpener import open as app_open, close as app_close
from commands.base_command import Command
from commands.photo_command import ScreenshotCommand

class OpenProgramCommand(Command):
    def __init__(self, bot,message,program_name:str, match_closest:bool=False):
        super().__init__(bot, message)
        self.program_name = program_name
        self.match_closest = match_closest

    def execute(self):
        try:
            self.send(f"{self.program_name} opened")
            app_open(self.program_name, match_closest=self.match_closest)
            ScreenshotCommand(self.bot, self.message).execute()
        except Exception as e:
            self.send(f"{self.program_name} failed. Reason: {e}")

class CloseProgramCommand(Command):
    def __init__(self, bot,message,program_name:str, match_closest:bool=False):
        super().__init__(bot, message)
        self.program_name = program_name
        self.match_closest = match_closest

    def execute(self):
        try:
            self.send(f"{self.program_name} closed")
            app_close(self.program_name, match_closest=self.match_closest)
            ScreenshotCommand(self.bot, self.message).execute()
        except Exception as e:
            self.send(f"{self.program_name} failed. Reason: {e}")