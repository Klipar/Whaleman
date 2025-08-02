import asyncio
from easy import Config, Logger
from tradingBot.coins.coinHab import CoinHab
from tradingBot.exchange.bybit import Bybit
from easy.message import *

from loggingBot.telegramLoggerClient import *

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
    asyncio.run(main())
