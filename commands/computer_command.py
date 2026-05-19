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
    """Перезагружает ПК."""

    def execute(self):
        try:
            self.send("🔄 Restarting in 10 seconds...\nType /cancel to abort.")
            subprocess.run(["shutdown", "/r", "/t", "10"])
        except Exception as e:
            self.send(f"ERROR RESTART: {e}")


class CancelShutdownCommand(Command):
    """Отменяет выключение или перезагрузку."""

    def execute(self):
        try:
            subprocess.run(["shutdown", "/a"])
            self.send("✅ Shutdown cancelled!")
        except Exception as e:
            self.send(f"ERROR CANCEL: {e}")

class StatsCommand(Command):
    """Выводит полную информацию о системе."""

    def execute(self):
        try:
            self.send(self._get_stats())
        except Exception as e:
            self.send(f"ERROR STATS: {e}")

    def _get_stats(self) -> str:
        # CPU
        cpu = psutil.cpu_percent(interval=1)
        cpu_cores = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        freq_str = f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A"

        # RAM
        ram = psutil.virtual_memory()
        ram_used = ram.used // (1024 ** 2)
        ram_total = ram.total // (1024 ** 2)

        # Диск
        disk = psutil.disk_usage("/")
        disk_used = disk.used // (1024 ** 3)
        disk_total = disk.total // (1024 ** 3)

        # Батарея
        battery = psutil.sensors_battery()
        if battery:
            charging = "🔌 Charging" if battery.power_plugged else "🔋 Battery"
            battery_str = f"{battery.percent:.0f}% {charging}"
        else:
            battery_str = "N/A"

        # Сеть
        net = psutil.net_io_counters()
        net_sent = net.bytes_sent // (1024 ** 2)
        net_recv = net.bytes_recv // (1024 ** 2)

        return (
            f"💻 System Stats\n"
            f"{'─' * 20}\n"
            f"🖥 CPU\n"
            f"  Load:  {cpu}%\n"
            f"  Cores: {cpu_cores}\n"
            f"  Freq:  {freq_str}\n\n"
            f"🧠 RAM\n"
            f"  Used:  {ram_used} MB / {ram_total} MB\n"
            f"  Load:  {ram.percent}%\n\n"
            f"💾 Disk\n"
            f"  Used:  {disk_used} GB / {disk_total} GB\n"
            f"  Load:  {disk.percent}%\n\n"
            f"🔋 Battery\n"
            f"  {battery_str}\n\n"
            f"🌐 Network\n"
            f"  Sent: {net_sent} MB\n"
            f"  Recv: {net_recv} MB"
        )


class ProcessesCommand(Command):
    """Выводит топ 30 процессов по CPU, без системных."""

    LIMIT = 30

    # Системные процессы которые скрываем
    SYSTEM_PROCS = {
        # Уже есть
        "system", "svchost.exe", "registry", "smss.exe", "csrss.exe",
        "wininit.exe", "services.exe", "lsass.exe", "winlogon.exe",
        "fontdrvhost.exe", "dwm.exe", "memory compression", "idle",
        "system interrupts", "ntoskrnl.exe", "conhost.exe", "spoolsv.exe",
        "runtimebroker.exe", "sihost.exe", "taskhostw.exe", "ctfmon.exe",
        "system idle process", "memcompression", "",

        # ← Добавь эти
        "wmiprvse.exe",  # Windows Management
        "msmpeng.exe",  # Windows Defender
        "nvsphelper64.exe",  # Nvidia helper
        "nvcontainer.exe",  # Nvidia container
        "nvdisplay.container.exe",  # Nvidia display
        "msedgewebview2.exe",  # Edge WebView (фон)
        "kndbwm.exe",  # HP сервис
        "kndbwmservice.exe",  # HP сервис
        "securityhealthservic.exe",  # Windows Security
        "systemsettingsbroker.exe",  # Windows Settings
        "intelcphdcpsvc.exe",  # Intel сервис
        "lsaiso.exe",  # Windows LSA
        "killeranalyticsservi.exe",  # Killer Network сервис
        "remotemouseservice.e",  # Remote Mouse сервис
    }
    def execute(self):
        try:
            self.send_html(self._get_processes())
        except Exception as e:
            self.send(f"ERROR PROCESSES: {e}")

    def _get_processes(self) -> str:
        procs = []
        # Первый вызов — "прогрев"
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
            try:
                proc.cpu_percent()  # первый вызов — всегда 0, игнорируем
            except:
                continue

        import time
        time.sleep(1)  # ждём 1 секунду

        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
            try:
                name = proc.info["name"] or ""
                # Пропускаем системные процессы
                if not name or name.lower() in self.SYSTEM_PROCS:
                    continue
                procs.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Сортируем по CPU, берём топ 30
        procs = sorted(procs, key=lambda x: x["cpu_percent"], reverse=True)
        procs = procs[:self.LIMIT]

        # Заголовок таблицы
        result = f"⚡ Top {self.LIMIT} Processes\n"
        result += f"{'─' * 30}\n"
        result += f" #  {'Name':<20} {'CPU':>5}  {'RAM':>7}\n"
        result += f"{'─' * 30}\n"

        for i, p in enumerate(procs, 1):
            name = (p["name"] or "")[:20]
            cpu = p["cpu_percent"]
            ram_mb = p["memory_info"].rss // (1024 ** 2) if p["memory_info"] else 0
            result += f"{i:>2}. {name:<20} {cpu:>4}%  {ram_mb:>5} MB\n"

        return f"<pre>{result}</pre>"