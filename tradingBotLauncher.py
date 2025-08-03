import asyncio
from multiprocessing import Process, Event
from typing import Any, Dict
from easy import Config, Logger
from loggingBot.telegramLoggerClient import TelegramLogger
from tradingBot.coins.coinHab import CoinHab
from tradingBot.exchange.bybit import Bybit
from easy.animations import SimpleAnimation
from easy.message import *

class TradingBotManager:
    def __init__(self, globalConfig: Config, socketClientConfig: Config, logger: Logger = None):
        self.logger = logger if logger else Logger()
        self.globalConfig = globalConfig
        self.socketClientConfig = socketClientConfig

        actionsHolder = {
            "Stop trading bot": self.stopTradingBot,
            "Start trading bot": self.startTradingBot,
            "Get status of whaleman bot": self.getTradingBotStatus}

        self.telegramLogger: TelegramLogger = TelegramLogger(self.socketClientConfig, actionsHolder)

        self.process = None

    async def startTradingBot(self, data: Dict[str, Any]):
        if self.process and self.process.is_alive():
            await self.telegramLogger.sendToUser(data["userID"], self.socketClientConfig.getValue("Commands", "startWhaleman", "already"))

        else:
            self.process = Process(target=self._run_bot_wrapper)
            self.process.start()

            await self.telegramLogger.sendToAll(self.socketClientConfig.getValue("Commands", "startWhaleman", "finished"))

    async def stopTradingBot(self, data: Dict[str, Any]):
        if self.process is None and not self.process.is_alive():
            await self.telegramLogger.sendToUser(data["userID"], self.socketClientConfig.getValue("Commands", "stopWhaleman", "already"))

        else:
            self.process.terminate()
            self.process.join()
            self.process = None

            await self.telegramLogger.sendToAll(self.socketClientConfig.getValue("Commands", "stopWhaleman", "finished"))

    async def getTradingBotStatus(self, data: Dict[str, Any]):
        if self.process and self.process.is_alive():
            await self.telegramLogger.sendToUser(data["userID"], self.socketClientConfig.getValue("Commands", "statusWhaleman", "working"))

        else:
            await self.telegramLogger.sendToUser(data["userID"], self.socketClientConfig.getValue("Commands", "statusWhaleman", "stopped"))

    async def getOpenOrders(self, data: Dict[str, Any]):
        pass

    def _run_bot_wrapper(self):
        asyncio.run(self._run_bot())

    async def _run_bot(self):
        try:
            await self.telegramLogger.sendToAll("Starting trading bot...")

            bybit = Bybit(self.globalConfig, self.telegramLogger)
            await bybit.refreshPositions()

            coin_hab = CoinHab(self.globalConfig, bybit)
            await coin_hab.initializeCoins(bybit)

            await bybit.subscribe(coin_hab)
            await self.telegramLogger.sendToAll("Bot started successfully!")

            while self.process and self.process.is_alive():
                await bybit.refreshPositions()
                await asyncio.sleep(5)

        except Exception as e:
            failed(f"Fail while running trading bot:\n{e}")

    async def runManager(self):
        animation = SimpleAnimation()
        try:
            while True:
                if not self.telegramLogger.isConnect():
                    self.logger.inform(f"Connecting to logging telegram bor [{animation.step()}]", en="\r")
                    try:
                        await self.telegramLogger.connect()

                    except Exception as e:
                        await asyncio.sleep(0.5)
                        continue
                else:
                    self.globalConfig = Config("Configs/tradingBot.json", Logger(2))
                    self.socketClientConfig = Config("Configs/telegramBot.json", Logger(2))
                    await asyncio.sleep(2)
        finally:
            await self.telegramLogger.disconnect()

async def main ():
    try:
        globalConfig = Config("Configs/tradingBot.json", Logger(2))
        socketClientConfig = Config("Configs/telegramBot.json", Logger(2))

        telegramLogger = TelegramLogger(socketClientConfig)
        await telegramLogger.connect()
        await telegramLogger.sendToAll("Starting trading bot...")

        bybit = Bybit(globalConfig, telegramLogger)
        await bybit.refreshPositions()

        coin_hab = CoinHab(globalConfig, bybit)
        await coin_hab.initializeCoins(bybit)

        await bybit.subscribe(coin_hab)

        await telegramLogger.sendToAll("Bot started successfully!")

        while True:
            await bybit.refreshPositions()
            globalConfig.refreshConfig()
            socketClientConfig.refreshConfig()

    except Exception as e:
        failed(f"Fail while running trading bot:\n{e}")
    finally:
        await telegramLogger.disconnect()

if __name__ == "__main__":
    tradingBotManager = TradingBotManager(Config("Configs/tradingBot.json", Logger(2)),
                                          Config("Configs/telegramBot.json", Logger(2)))

    asyncio.run(tradingBotManager.runManager())
