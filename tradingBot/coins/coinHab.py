from easy import failed, inform, Config
from typing import Dict
import asyncio
from tradingBot.exchange.bybit import Bybit
from easy.animations import *
from tradingBot.coins.coin import Coin

class CoinHab:
    def __init__(self, conf: Config, bybit: Bybit):
        self.animation = SimpleAnimation()

        self.coins: Dict[str, Coin] = {}

        self.trashText = f"kline.{conf.getValue('exchange', 'Trade', 'Candle time')}." # extra text that comes in response from the socket. It is removed to leave only the coin name

        self.coinSet (conf, bybit)
        self.setRounding(conf, bybit)

        inform (f"Founded {len(self.coins)} Coins")

    def setRounding(self, conf, bybit: Bybit):
        response = bybit.getInstrumentsInfo()
        for i in response["result"]["list"]:
            for j in ((conf.getValue("exchange", "Coins"))):
                if (i["symbol"] == j):
                    self.coins[j].setRounding(i)

    def handler(self, message):
        inform(self.animation.step(), en="\r")
        asyncio.run(self.coins[message['topic'].replace(self.trashText, "")].processValues(message))


    async def initializeCoins (self, bybit: Bybit):
        result = await bybit.getClineForAll()

        for i in range (len(self.coins)):
            if (int(result[i]['retCode']) == 0):
                self.coins[result[i]['result']['symbol']].initialize(result[i])
            else:
                failed (result[i])

    def coinSet (self, conf: Config, bybit: Bybit):
        for coin in ((conf.getValue("exchange", "Coins"))):
            self.coins[coin] = Coin(conf, coin, bybit)
