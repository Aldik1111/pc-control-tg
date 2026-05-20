# 🤖 PC Control Bot

A Telegram bot that lets you control your computer remotely from your phone. Built as a final project for Introduction to Programming 2 at Astana IT University.

---

## What it does

The idea is simple — you open Telegram on your phone and control your PC without touching it. Take a screenshot to see what's on the screen, open or close apps, check how much RAM is being used, shut down the computer before leaving home, or just check the weather. Everything through buttons in Telegram.

Here's a full list of what the bot can do:

| Category | Features |
|---|---|
| 📷 Photo | Screenshot, webcam photo |
| 💻 Programs | Open / close Chrome, Steam, Spotify, WhatsApp, or any other app |
| 📊 Monitor | CPU load, RAM, disk, battery, network, top 30 processes |
| 🌤 Weather | Current weather by city name (wttr.in API) |
| 🔴 Power | Shutdown, restart, sleep, lock screen |
| 📝 Notes | Add, view, delete notes by number |
| 📊 History | Last 5 actions from the log |
| 📷 Receive photo | Send a photo to the bot and it saves it on your PC |
| 🔐 Auth | Only the owner can use the bot |

---

## How to run it

**1. Clone the repo**
```bash
git clone https://github.com/your-username/pc-control-bot.git
cd pc-control-bot
```

**2. Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file**
```
BOT_TOKEN=your_token_from_BotFather
OWNER_ID=your_telegram_user_id
```

To find your user ID — message `@userinfobot` in Telegram, it will tell you.

**5. Run**
```bash
python main.py
```

---

## Project structure

```
pc_control_bot/
├── main.py                    # Entry point — just starts the bot
├── requirements.txt
├── README.md
├── .env                       # Token and owner ID — never push this to GitHub
├── .gitignore
│
├── bot/
│   ├── handlers.py            # All message handlers
│   ├── keyboards.py           # All keyboards
│   └── auth.py                # Owner check
│
├── commands/
│   ├── base_command.py        # Abstract base class Command
│   ├── photo_command.py       # WebCamCommand, ScreenshotCommand
│   ├── program_command.py     # OpenProgramCommand, CloseProgramCommand
│   ├── computer_command.py    # Stats, Processes, Shutdown, Restart, Sleep, Lock
│   └── weather_command.py     # WeatherCommand — calls wttr.in API
│
├── data/
│   ├── logger.py              # Action logging + log_generator()
│   ├── notes.py               # Notes CRUD
│   ├── log.json               # Action history
│   └── notes.json             # Saved notes
│
├── utils/
│   └── decorators.py          # @owner_required, @log_command, @retry
│
└── tests/
    ├── test_logger.py         # 12 tests
    ├── test_commands.py       #  6 tests
    ├── test_notes.py          # 10 tests
    └── test_weather.py        #  4 tests
```

---

## How it's built

### OOP

Every action in the bot is a class. They all inherit from an abstract base class called `Command`, which lives in `commands/base_command.py`. The base class defines the interface — every subclass must implement `execute()`, otherwise Python will throw an error. It also provides two shared methods: `send()` for text and `send_photo()` for images, so we don't repeat that code everywhere.

```
Command (ABC)
├── execute()        ← abstract, required in every subclass
├── send()           ← sends text to the user
└── send_photo()     ← sends a photo to the user
      │
      ├── WebCamCommand
      ├── ScreenshotCommand
      ├── OpenProgramCommand
      ├── CloseProgramCommand
      ├── StatsCommand
      ├── ProcessesCommand
      ├── ShutdownCommand
      ├── RestartCommand
      ├── SleepCommand
      ├── LockCommand
      └── WeatherCommand
```

### Decorators

Instead of writing `owner_only()` and `log_action()` manually in every single handler, we use decorators. Every handler in `handlers.py` looks like this:

```python
@bot.message_handler(func=lambda m: m.text == "🖥 Screenshot")
@owner_required(bot)
@log_command("Screenshot")
def handle_screenshot(message):
    cmd = ScreenshotCommand(bot, message)
    cmd.execute()
```

Three decorators in `utils/decorators.py`:

- `@owner_required(bot)` — checks if the message is from the owner, sends "🚫 Access denied" if not
- `@log_command("action")` — writes the action to `log.json` and prints execution time to console
- `@retry(times=3)` — retries the function up to 3 times if it fails, used in the weather API call

### Generator

`log_generator(n)` in `data/logger.py` uses `yield` to return log entries one by one instead of loading everything into memory at once. It's used inside `get_last_logs()` to build the history message:

```python
def log_generator(n: int = 5):
    entries = _read_log()
    for entry in entries[-n:]:
        yield entry
```

### External API

Weather data comes from [wttr.in](https://wttr.in) — a free weather API, no registration needed. The bot sends a GET request and parses the JSON response to show temperature, humidity, wind, pressure and condition.

The `@retry(times=3)` decorator is applied to the fetch method, so if the network is slow or the request fails, it tries again automatically up to 3 times.

### Data persistence

Two JSON files store data between sessions:

- `log.json` — every action the owner takes is logged here with user ID, action name, and timestamp
- `notes.json` — personal notes with auto-incremented IDs, so you can delete them by number

### Security

The owner's Telegram user ID is stored in `.env` and never in the code. The `.env` file is in `.gitignore` so it never ends up on GitHub. Any message from someone who isn't the owner gets blocked immediately — the bot replies with "🚫 Access denied" and does nothing.

---

## Tests

```bash
python -m unittest discover tests/
```

Expected output:
```
................................
Ran 32 tests in 0.1s
OK
```

Mock objects are used to simulate the camera, screenshot tool, AppOpener, and HTTP requests — so tests run without any hardware or internet connection.

---

## Tech stack

| Library | What it's used for |
|---|---|
| `pyTelegramBotAPI` | Telegram Bot API |
| `opencv-python` | Webcam capture |
| `pyautogui` | Screenshots |
| `AppOpener` | Open and close applications |
| `psutil` | System monitoring |
| `requests` | HTTP requests to wttr.in |
| `python-dotenv` | Load token and owner ID from .env |
| `unittest` | Testing |
