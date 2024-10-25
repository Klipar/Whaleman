from telegram.ext import Application, CommandHandler, CallbackContext
from telegram import Update
from telegram import Bot
from multiprocessing import Process
import asyncio
import os
from easy.massage import failed, success, inform, warn, test


from time import sleep

class TeleGramLogBot:
    def __init__(self, autostart = False):
        inform ("Initializing the bot...")
        self.TOKEN = '7173552290:AAECYbttByqVWlGaUsmjTc0Ur7wXCFB9rLk'
        self.file_path = "user_ids.txt"

        self.user_ids = set()  # Список для зберігання user_id користувачів
        self.application = Application.builder().token(self.TOKEN).build()
        self._setup_handlers()
        self._load_user_ids()  # Зчитуємо user_id з файлу при запуску
        self.bot = Bot(token=self.TOKEN)
        self.process = None

        self.start_massage = "You are successfully subscribed to receive messages from the bot."
        self.stop_massage  = "You have successfully unsubscribed from receiving messages from the bot."
        self.info_massage  = "BOT V = 2.0.0"
        self.help_massage  = "Available commands:\n/start —> subscribe to receive messages.\n/stop —> unsubscribe from receiving messages.\n/info —> get information about the bot.\n/help —> display this message."
        self.start_massage_enother_time = "You are already subscribed."
        self.stop_massage_enother_time  = "You are already unsubscribed."
        success("Bot initialized successfully")
        if autostart:
            self.run()

    def _setup_handlers(self): #Налаштування обробників команд.
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("info", self.info))
        self.application.add_handler(CommandHandler("help", self.help))

    def _load_user_ids(self):   #Зчитування user_id з файлу
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    self.user_ids = set()
                    for line in file:
                        user_id = line.strip()
                        if user_id.isdigit():
                            self.user_ids.add(int(user_id))
            except Exception as e:
                failed(f"Failed to load user database... ERROR: {e}")

    def _save_user_ids(self):     #Запис user_id у файл
        with open(self.file_path, "w") as file:
            for user_id in self.user_ids:
                file.write(f"{user_id}\n")

    async def start(self, update: Update, context: CallbackContext) -> None: #Обробляє команду /start.
        user_id = update.message.chat_id
        if user_id not in self.user_ids:
            self.user_ids.add(user_id)  # Додаємо користувача до списку
            self._save_user_ids()  # Записуємо у файл
            await update.message.reply_text(self.start_massage)
        else:
            await update.message.reply_text(self.start_massage_enother_time)

    async def info(self, update: Update, context: CallbackContext) -> None: #Обробляє команду /start.
        await update.message.reply_text(self.info_massage)

    async def help(self, update: Update, context: CallbackContext) -> None: #Обробляє команду /start.
        await update.message.reply_text(self.help_massage)

    async def stop(self, update: Update, context: CallbackContext) -> None: #Обробляє команду /stop
        user_id = update.message.chat_id
        if user_id in self.user_ids:
            self.user_ids.remove(user_id)  # Видаляємо користувача зі списку
            self._save_user_ids()  # Оновлюємо файл
            await update.message.reply_text(self.stop_massage)
        else:
            await update.message.reply_text(self.stop_massage_enother_time)

    async def SEND_messager_to_all(self, message="hello!)"): # Надсилання повідомлень
        for user_id in self.user_ids:
            try:
                await self.bot.send_message(chat_id=user_id, text=message)
                # failed(f"Повідомлення надіслано користувачу {user_id}")
            except Exception as e:
                failed(f"Error sending message to user {user_id}: {e}")
                # Try_All_Clean (message)

    def SEND_TG(self, test = "TEST..."):
        self._load_user_ids()
        asyncio.run(self.SEND_messager_to_all(test))

    def run(self):          #Запуск бота
        inform("Starting Bot...")
        self.process = Process(target=self.application.run_polling)
        self.process.start()
        success("Bot started!")
    def terminate(self):         #зупинка бота
        inform("Stopping Bot...")
        self.process.terminate()
        success("Bot stopped!")
# Використання класу:



def TG_LOG(text):
    with open('TRANSFER', 'a') as file:
        # Додаємо дані до файлу
        file.write(text + "\n")

def TG_LOG_ORDER(side, prise, takeProfit, stopLoss, symbol, qty, leverage):
    Value = round((qty*prise), 2)
    profit = (round((((abs((takeProfit*qty)-(prise*qty))))*leverage), 2))
    losis  = (round((((abs((stopLoss*qty)-(prise*qty)))*-1)*leverage), 2))
    LONG = f'''
    ❗️❗️❗️️  PLACING ORDER  ❗️❗️❗️
    ============================
                    🟢 LONG 🟢
            Symbol:     {symbol}
            Side:           Buy    
            Trigering prise = {prise}
            Take profit        = {takeProfit}
            Stop lose          = {stopLoss}
    -----------------------------------------------------
            Qty                      = {qty}
            Value in USDT  = {Value}
            Order tipe          = Limit
            Trade fee           = ?
    -----------------------------------------------------
                Expected profit      = {profit}
                Expected losses    = {losis}
    ============================
    '''
    SHORT = f'''
    ❗️❗️❗️️  PLACING ORDER  ❗️❗️❗️
    ============================
                        🔴 Short 🔴
                Symbol:     {symbol}
                Side:           Sell    
                Trigering prise = {prise}
                Take profit        = {takeProfit}
                Stop lose          = {stopLoss}
    -----------------------------------------------------
                Qty                      = {qty}
                Value in USDT  = {Value}
                Order tipe          = Limit
                Trade fee           = ?
    -----------------------------------------------------
                Expected profit      = {profit}
                Expected losses    = {losis}
    ============================
    '''
    if (side == "Buy"): TG_LOG(LONG)
    else:               TG_LOG(SHORT)



def START_TELE_BOT():
    filename = 'TRANSFER'
    old_content = ""
    bot = TeleGramLogBot(True)
    while 1:

        # Перевірка існування файлу
        
        if os.path.exists(filename):
            # Якщо файл існує, зчитуємо його вміст
            with open(filename, 'r') as file:
                content = file.read()
            if (old_content != content):
                bot.terminate()
                del bot
                bot = TeleGramLogBot(True)
                bot.SEND_TG(content)
                print("Content:\n", content)
                os.remove(filename)
            old_content = content
        sleep (1)

def BOT_LAUNCHER():
    while (1):
        pp = Process(target=START_TELE_BOT)
        pp.start()
        pp.join()
    # Бот запускається і працює у фоновому режимі
    # bot.run()

    # Приклад виклику методу відправки повідомлення всім підписникам
    # for i in range (0, 100):
    #     bot.SEND_TG(f"TESTING for => {i}")
    # bot.SEND_TG(f"GOOOOOOD)")
    # bot.terminate()



# from multiprocessing import Process
# from time import sleep
# # Функція, яку будемо запускати в окремому процесі
# def my_function():
#     print("Процес виконується!")
#     sleep(30)
#     print("Процес завершився!")

# # Створення нового процесу
# process = Process(target=my_function)

# # Запуск процесу
# process.start()

# # Очікування завершення процесу
# # process.join()
# sleep(5)
# process.terminate()
# print("Процес")

