from telegram.ext import Application, CommandHandler, CallbackContext
from telegram import Update
from telegram import Bot
from multiprocessing import Process
import asyncio
import os
from easy.message import *


from time import sleep

class TeleGramLogBot:
    def __init__(self, autostart = False):
        inform ("Initializing the bot...")
        self.TelegramAPIToken = '7173552290:AAECYbttByqVWlGaUsmjTc0Ur7wXCFB9rLk'
        self.filePath = "user_ids.txt"

        self.userIds = set()
        self.application = Application.builder().token(self.TelegramAPIToken).build()
        self._setupHandlers()
        self._loadUserIds()
        self.bot = Bot(token=self.TelegramAPIToken)
        self.process = None

        self.startMessage = "You are successfully subscribed to receive messages from the bot."
        self.stopMessage  = "You have successfully unsubscribed from receiving messages from the bot."
        self.infoMessage  = "BOT V = 2.0.0"
        self.helpMessage  = "Available commands:\n/start —> subscribe to receive messages.\n/stop —> unsubscribe from receiving messages.\n/info —> get information about the bot.\n/help —> display this message."
        self.startMessageAnotherTime = "You are already subscribed."
        self.stopMessageAnotherTime  = "You are already unsubscribed."
        success("Bot initialized successfully")
        if autostart:
            self.run()

    def _setupHandlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("info", self.info))
        self.application.add_handler(CommandHandler("help", self.help))

    def _loadUserIds(self):
        if os.path.exists(self.filePath):
            try:
                with open(self.filePath, "r") as file:
                    self.userIds = set()
                    for line in file:
                        userId = line.strip()
                        if userId.isdigit():
                            self.userIds.add(int(userId))
            except Exception as e:
                failed(f"Failed to load user database... ERROR: {e}")

    def _saveUserIds(self):
        with open(self.filePath, "w") as file:
            for userId in self.userIds:
                file.write(f"{userId}\n")

    async def start(self, update: Update, context: CallbackContext) -> None:
        userId = update.message.chat_id
        if userId not in self.userIds:
            self.userIds.add(userId)
            self._saveUserIds()
            await update.message.reply_text(self.startMessage)
        else:
            await update.message.reply_text(self.startMessageAnotherTime)

    async def info(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text(self.infoMessage)

    async def help(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text(self.helpMessage)

    async def stop(self, update: Update, context: CallbackContext) -> None:
        userId = update.message.chat_id
        if userId in self.userIds:
            self.userIds.remove(userId)
            self._saveUserIds()
            await update.message.reply_text(self.stopMessage)
        else:
            await update.message.reply_text(self.stopMessageAnotherTime)

    async def sendMessageToAll(self, message="hello!)"):
        for userId in self.userIds:
            try:
                await self.bot.send_message(chat_id=userId, text=message)

            except Exception as e:
                failed(f"Error sending message to user {userId}: {e}")

    def sendTG(self, text="TEST..."):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(self.sendMessageToAll(text))
        else:
            loop.run_until_complete(self.sendMessageToAll(text))

    def _runPolling(self):
        asyncio.run(self.application.run_polling())

    def run(self):
        inform("Starting Bot...")
        self.process = Process(target=self._runPolling)
        self.process.start()
        success("Bot started!")

    def terminate(self):
        inform("Stopping Bot...")
        self.process.terminate()
        success("Bot stopped!")


def logTG(text):
    with open('TRANSFER', 'a') as file:
        file.write(text + "\n")

def logOrderTG(side, prise, takeProfit, stopLoss, symbol, qty, leverage):
    Value = round((qty*prise), 2)
    profit = (round((((abs((takeProfit*qty)-(prise*qty))))*leverage), 2))
    loss  = (round((((abs((stopLoss*qty)-(prise*qty)))*-1)*leverage), 2))
    LONG = f'''
    ❗️❗️❗️️  PLACING ORDER  ❗️❗️❗️
    ============================
                    🟢 LONG 🟢
            Symbol:     {symbol}
            Side:           Buy
            Triggering prise = {prise}
            Take profit        = {takeProfit}
            Stop lose          = {stopLoss}
    -----------------------------------------------------
            Qty                      = {qty}
            Value in USDT  = {Value}
            Order type          = Limit
            Trade fee           = ?
    -----------------------------------------------------
                Expected profit      = {profit}
                Expected losses    = {loss}
    ============================
    '''
    SHORT = f'''
    ❗️❗️❗️️  PLACING ORDER  ❗️❗️❗️
    ============================
                        🔴 Short 🔴
                Symbol:     {symbol}
                Side:           Sell
                Triggering prise = {prise}
                Take profit        = {takeProfit}
                Stop lose          = {stopLoss}
    -----------------------------------------------------
                Qty                      = {qty}
                Value in USDT  = {Value}
                Order type          = Limit
                Trade fee           = ?
    -----------------------------------------------------
                Expected profit      = {profit}
                Expected losses    = {loss}
    ============================
    '''
    if (side == "Buy"): logTG(LONG)
    else:               logTG(SHORT)


def startTGBot():
    filename = 'TRANSFER'
    oldContent = ""
    bot = TeleGramLogBot(True)
    while 1:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                content = file.read()
            if (oldContent != content):
                bot.sendTG(content)
                os.remove(filename)
            oldContent = content
        sleep(1)

if __name__ == "__main__":
    startTGBot()
