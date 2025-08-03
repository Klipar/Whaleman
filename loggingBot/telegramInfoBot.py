from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder
from telegram import Update
from telegram import Bot
from typing import Any, Dict, List
import asyncio
from easy import Config, Logger
from loggingBot.positionMessageSynthesizer import PositionMessageSynthesizer
from loggingBot.database.telegramUsersDatabase import TelegramUsersDatabase
from loggingBot.socket.socketServer import SocketServer

class TeleGramLogBot:
    def __init__(self, config: Config, database: TelegramUsersDatabase, logger: Logger = Logger()):
        self.logger = logger
        self.config = config
        self.database = database

        self.socketServer: SocketServer = None

        self.logger.inform ("Initializing Telegram Logging bot...")

        self.application = (
            ApplicationBuilder()
            .token(self.config.getValue("Telegram API token"))
            .post_init(self.onStartup)
            .build()
        )
        self._setupHandlers()
        self.bot = Bot(token=self.config.getValue("Telegram API token"))

        self.positionMessageSynthesizer = PositionMessageSynthesizer(config=config,logger=logger)

        self.logger.success("Telegram bot initialized successfully")

    async def onStartup(self, app):
        async def sendMassageToAll(data: Dict[str, Any]):
            await self.sendMessageToAll(data["message"], self.database.getTelegramIDForAllSubscribedUsers())

        async def sendMassageToAdmins(data: Dict[str, Any]):
            await self.sendMessageToAll(data["message"], self.database.getTelegramIDForAllSubscribedAdmins())

        async def sendPlacingOrder(data: Dict[str, Any]):
            await self.sendMessageToAll(self.positionMessageSynthesizer.getSynthesizerOrderMessage(data),
                                        self.database.getTelegramIDForAllSubscribedUsers())

        async def sendMassageToUser(data: Dict[str, Any]):
            await self.sendToUser(data["userID"], data["message"])

        actionsHolder = {
            "Send to all" : sendMassageToAll,
            "Send to admins" : sendMassageToAdmins,
            "Place order" : sendPlacingOrder,
            "Send to user" : sendMassageToUser
        }

        self.socketServer = SocketServer(config=self.config,
                                         actionsHolder=actionsHolder,
                                         logger=self.logger)

        asyncio.create_task(self.socketServer.start())

    def _setupHandlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("info", self.info))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("stopWhaleman", self.stopWhaleman))
        self.application.add_handler(CommandHandler("startWhaleman", self.startWhaleman))
        self.application.add_handler(CommandHandler("statusWhaleman", self.statusWhaleman))
        self.application.add_handler(CommandHandler("showOpenOrders", self.showOpenOrders))

    async def start(self, update: Update, context: CallbackContext) -> None:
        TelegramID = update.message.chat_id
        user = self.database.getUser(TelegramID)
        if user is not None and user[1] == 1:
            await update.message.reply_text(self.config.getValue("Commands", "start", "already"))
        else:
            if user is None:
                self.database.addOrUpdateUser(TelegramID=TelegramID, subscribed=1, sudo=0)
            else:
                self.database.addOrUpdateUser(TelegramID=TelegramID, subscribed=1, sudo=user[2])
            await update.message.reply_text(self.config.getValue("Commands", "start", "success"))

    async def stopWhaleman(self, update: Update, context: CallbackContext) -> None:
        TelegramID = update.message.chat_id
        if TelegramID in self.database.getTelegramIDForAllSubscribedAdmins():
            templates = self.config.getValue("Socket server", "Massages", "Stop trading bot")
            templates["data"]["userID"] = TelegramID

            await self.socketServer.broadcast(templates)
            await update.message.reply_text(self.config.getValue("Commands", "stopWhaleman", "success"))

        else:
            await update.message.reply_text(self.config.getValue("Commands", "stopWhaleman", "failed"))

    async def startWhaleman(self, update: Update, context: CallbackContext) -> None:
        TelegramID = update.message.chat_id
        if TelegramID in self.database.getTelegramIDForAllSubscribedAdmins():
            templates = self.config.getValue("Socket server", "Massages", "Start trading bot")
            templates["data"]["userID"] = TelegramID

            await self.socketServer.broadcast(templates)
            await update.message.reply_text(self.config.getValue("Commands", "startWhaleman", "success"))

        else:
            await update.message.reply_text(self.config.getValue("Commands", "startWhaleman", "failed"))

    async def statusWhaleman(self, update: Update, context: CallbackContext) -> None:
        TelegramID = update.message.chat_id
        if TelegramID in self.database.getTelegramIDForAllSubscribedAdmins():
            templates = self.config.getValue("Socket server", "Massages", "Get status of whaleman bot")
            templates["data"]["userID"] = TelegramID

            await self.socketServer.broadcast(templates)
            await update.message.reply_text(self.config.getValue("Commands", "statusWhaleman", "success"))

        else:
            await update.message.reply_text(self.config.getValue("Commands", "statusWhaleman", "failed"))

    async def showOpenOrders(self, update: Update, context: CallbackContext) -> None:
        TelegramID = update.message.chat_id
        if TelegramID in self.database.getTelegramIDForAllSubscribedAdmins():
            templates = self.config.getValue("Socket server", "Massages", "Get open orders")
            templates["data"]["userID"] = TelegramID

            await self.socketServer.broadcast(templates)
            await update.message.reply_text(self.config.getValue("Commands", "showOpenOrders", "success"))

        else:
            await update.message.reply_text(self.config.getValue("Commands", "showOpenOrders", "failed"))

    async def info(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text(self.config.getValue("Commands", "info", "success"))

    async def help(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text(self.config.getValue("Commands", "help", "success"))

    async def stop(self, update: Update, context: CallbackContext) -> None:
        TelegramID = update.message.chat_id
        user = self.database.getUser(TelegramID)
        if user is not None and user[1] == 1:
            self.database.addOrUpdateUser(TelegramID=TelegramID, subscribed=0, sudo=user[2])
            await update.message.reply_text(self.config.getValue("Commands", "stop", "success"))
        else:
            if user is not None:
                await update.message.reply_text(self.config.getValue("Commands", "stop", "already"))
            else:
                self.database.addOrUpdateUser(TelegramID=TelegramID, subscribed=0, sudo=0)
                await update.message.reply_text(self.config.getValue("Commands", "stop", "never"))

    async def sendToUser(self, user_id: int, message: str):
        try:
            await self.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            self.logger.warn(f"Failed to send message to: {user_id}: {e}")

    async def sendMessageToAll(self, message: str, users: List[int], maxConcurrent=10):
        sem = asyncio.Semaphore(maxConcurrent)

        async def semTask(user_id):
            async with sem:
                await self.sendToUser(user_id, message)

        await asyncio.gather(*(semTask(uid) for uid in users))

    def run(self):
            self.application.run_polling()
