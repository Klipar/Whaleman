import asyncio
from easy import Config
from coinHab import CoinHab
from bybit import Bybit
from easy.message import *

async def main ():
    config = Config("Configs/developing.json")

    bybit = Bybit(config)

    coin_hab = CoinHab(config, bybit)
    await coin_hab.initializeCoins(bybit)

    await bybit.Subscribe(coin_hab)

    while True:
        bybit.Refresh_Positions()
        # config.refreshConfig()

if __name__ == "__main__":
    asyncio.run(main())
