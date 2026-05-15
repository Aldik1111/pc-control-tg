from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.chat_id = message.chat.id

    @abstractmethod
    def execute(self):
        pass

    def send(self, text:str):
        self.bot.send_message(self.chat_id, text)

    def send_photo(self,path:str):
        with open(path,'rb') as f:
            self.bot.send_photo(self.chat_id, f)