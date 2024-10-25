import os
from telegram import Bot
import asyncio

class Tele:
    def __init__(self):        
        self.TOKEN = '7173552290:AAECYbttByqVWlGaUsmjTc0Ur7wXCFB9rLk'
        self.PATH = "user_ids.txt"
        self.bot = Bot(token=self.TOKEN)

        self.user_ids = set()
    
    def loadID(self):
        # Перевірка наявності файлу
        if not os.path.exists(self.PATH):
            print(f"Файл {self.PATH} не знайдено.")
            return

        # Читання user_id з файлу
        self.user_ids = set()
        with open(self.PATH, "r") as file:
            for line in file:
                user_id = line.strip()
                if user_id.isdigit():
                    self.user_ids.add(int(user_id))

    async def SEND(self, message="hello!)"):
        # Надсилання повідомлень
        for user_id in self.user_ids:
            try:
                await self.bot.send_message(chat_id=user_id, text=message)
                print(f"Повідомлення надіслано користувачу {user_id}")
            except Exception as e:
                print(f"Помилка при відправці повідомлення користувачу {user_id}: {e}")

# Запуск асинхронного циклу для надсилання повідомлень
if __name__ == '__main__':
    t = Tele()  # Створення екземпляра класу
    t.loadID()  # Завантаження ID користувачів

    # Виклик асинхронної функції
    asyncio.run(t.SEND("lololo"))