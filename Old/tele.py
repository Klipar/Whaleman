import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio

class TeleGramSend:
    def __init__(self, token: str, file_path: str):
        self.token = token
        self.file_path = file_path
        self.user_ids = set()  # Список для зберігання user_id користувачів
        self.application = Application.builder().token(self.token).build()
        self._setup_handlers()
        self._load_user_ids()  # Зчитуємо user_id з файлу при запуску

    def _setup_handlers(self):
        """Налаштування обробників команд."""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stop", self.stop))

    def _load_user_ids(self):
        """Зчитування user_id з файлу."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                for line in file:
                    user_id = line.strip()
                    if user_id.isdigit():
                        self.user_ids.add(int(user_id))

    def _save_user_ids(self):
        """Запис user_id у файл."""
        with open(self.file_path, "w") as file:
            for user_id in self.user_ids:
                file.write(f"{user_id}\n")

    async def start(self, update: Update, context: CallbackContext) -> None:
        """Обробляє команду /start."""
        user_id = update.message.chat_id
        if user_id not in self.user_ids:
            self.user_ids.add(user_id)  # Додаємо користувача до списку
            self._save_user_ids()  # Записуємо у файл
        await update.message.reply_text("Ви підписані на повідомлення!")

    async def stop(self, update: Update, context: CallbackContext) -> None:
        """Обробляє команду /stop."""
        user_id = update.message.chat_id
        if user_id in self.user_ids:
            self.user_ids.remove(user_id)  # Видаляємо користувача зі списку
            self._save_user_ids()  # Оновлюємо файл
            await update.message.reply_text("Ви більше не будете отримувати повідомлення.")
        else:
            await update.message.reply_text("Вас немає в списку підписників.")

    async def _send_message_to_all(self, message: str) -> None:
        """Функція для надсилання повідомлення всім підписникам."""
        for user_id in self.user_ids:
            try:
                await self.application.bot.send_message(chat_id=user_id, text=message)
            except Exception as e:
                print(f"Помилка при відправці повідомлення користувачу {user_id}: {e}")

    def send_message_to_all(self, message: str):
        """Виклик функції надсилання повідомлення."""
        asyncio.create_task(self._send_message_to_all(message))

    def run(self):
        """Запуск бота."""
        self.application.run_polling()

# Використання класу:
if __name__ == '__main__':
    TOKEN = '7173552290:AAECYbttByqVWlGaUsmjTc0Ur7wXCFB9rLk'

    FILE_PATH = "user_ids.txt"  # Шлях до файлу для зберігання user_id

    bot = TeleGramSend(TOKEN, FILE_PATH)
    
    # Бот запускається і працює у фоновому режимі
    bot.run()

    # Приклад виклику методу відправки повідомлення всім підписникам
    bot.send_message_to_all("Я зараз тистуватиму роботу бота тому можуть приходити сміттєві повідомлення. Можеш ввести /stop щоб тимчасово відписатись")