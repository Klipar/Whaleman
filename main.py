import asyncio
from easy import Config, Logger
from coinHab import CoinHab
from bybit import Bybit
from easy.message import *

from telegramLogger import *

async def main ():
    globalConfig = Config("Configs/developing.json", Logger(2))
    socketClientConfig = Config("Configs/telegramBot.json", Logger(2))

    telegramLogger = TelegramLogger(socketClientConfig)
    await telegramLogger.connect()
    await telegramLogger.sendToAll("Starting trading bot...")

    bybit = Bybit(globalConfig, telegramLogger)

    coin_hab = CoinHab(globalConfig, bybit)
    await coin_hab.initializeCoins(bybit)

    await bybit.subscribe(coin_hab)

    await telegramLogger.sendToAll("Bot started successfully!")

    while True:
        bybit.refreshPositions()
        # config.refreshConfig()

if __name__ == "__main__":
    asyncio.run(main())
