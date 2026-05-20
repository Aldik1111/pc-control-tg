import psutil
from commands.base_command import Command
import subprocess

class ShutdownCommand(Command):
    """Выключает ПК."""

    def execute(self):
        try:
            self.send("🔴 Shutting down in 10 seconds...\nType /cancel to abort.")
            subprocess.run(["shutdown", "/s", "/t", "10"])
        except Exception as e:
            self.send(f"ERROR SHUTDOWN: {e}")


class RestartCommand(Command):
    def execute(self):
        try:
            self.send("🔄 Restarting in 10 seconds...\nType /cancel to abort.")
            subprocess.run(["shutdown", "/r", "/t", "10"])
        except Exception as e:
            self.send(f"ERROR RESTART: {e}")

class SleepCommand(Command):
    def execute(self):
        try:
            self.send("😴 Sleeping...")
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
        except Exception as e:
            self.send(f"ERROR SLEEP: {e}")


class LockCommand(Command):
    def execute(self):
        try:
            self.send("🔒 Locking screen...")
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        except Exception as e:
            self.send(f"ERROR LOCK: {e}")


class CancelShutdownCommand(Command):
    """Отменяет выключение или перезагрузку."""

    def execute(self):
        try:
            subprocess.run(["shutdown", "/a"])
            self.send("✅ Shutdown cancelled!")
        except Exception as e:
            self.send(f"ERROR CANCEL: {e}")
