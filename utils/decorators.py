import os
import time
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
OWNER_ID = int(os.getenv("OWNER_ID", 0))


def owner_required(bot):
    def decorator(func):
        @wraps(func)
        def wrapper(message, *args, **kwargs):
            if message.from_user.id != OWNER_ID:
                bot.send_message(message.chat.id, "🚫 Access denied.")
                print(f"[AUTH] Blocked user {message.from_user.id}")
                return
            return func(message, *args, **kwargs)
        return wrapper
    return decorator


def log_command(action: str):
    def decorator(func):
        @wraps(func)
        def wrapper(message, *args, **kwargs):
            from data.logger import log_action
            # Лог в файл
            log_action(message.from_user.id, action)
            # Время выполнения в консоль
            start = time.time()
            print(f"[CMD] {action} started")
            result = func(message, *args, **kwargs)
            elapsed = time.time() - start
            print(f"[CMD] {action} finished in {elapsed:.2f}s")
            return result
        return wrapper
    return decorator



def retry(times=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] Attempt {attempt}/{times} failed: {e}")
                    if attempt < times:
                        time.sleep(delay)
            raise Exception(f"All {times} attempts failed.")
        return wrapper
    return decorator