from typing import Dict
from easy import failed, inform, Config
import asyncio
from bybit import Bybit
from easy.animations import *

from queueManager import QueueManager

class Coin:
    def __init__(self, config: Config, coin: str, bybit: Bybit):
        from conditions import checkOrderConditions
        self.checkOrderConditions = checkOrderConditions

        self.bybit: Bybit = bybit
        self.config: Config = config

        self.coin: str = coin

    def roundQty (self, qty):
        return (round(float(qty) / self.qtyStepForRound) * self.qtyStepForRound)

    def roundPrise (self, prise):
        return round(float(prise), self.priseRound)

    def setRound(self, response):
        self.priseRound = int(response['priceScale'])
        self.qtyStepForRound = float(response['lotSizeFilter']['qtyStep'])

    def processValues(self, data):
        data['data'].sort(key=lambda x: x["start"])

        for data in data['data']:
            self.pricesQueueManager.updateQueue(data)

        self.checkOrderConditions(self)

    def initialize (self, data):
        self.pricesQueueManager = QueueManager(data)

    def getLastPrise (self):
        return self.pricesQueueManager.getLatest().close

class CoinHab:
    def __init__(self, conf: Config, bybit: Bybit):
        self.animation = SimpleAnimation()
        self.coins: Dict[str, Coin] = {}
        self.trashText = f"kline.{conf.getValue("exchange", "Trade", "Candle time")}." # зайвий текст що приходить в відповіді від сокета. Він видаляється щоб лишити лише назву монети
        self.coinSet (conf, bybit)
        self.SetRounds(conf, bybit)
        inform (f"Founded {len(self.coins)} Coins")

    def SetRounds(self, conf, bybit: Bybit):
        response = bybit.Get_Instruments_Info()
        for i in response["result"]["list"]:
            for j in ((conf.getValue("exchange", "Coins"))):
                if (i["symbol"] == j):
                    self.coins[j].setRound(i)

    def handler(self, message):
        inform(self.animation.step(), en="\r")
        self.coins[message['topic'].replace(self.trashText, "")].processValues(message)


    def Initialize_Coins (self, conf: Config, bybit: Bybit):
        result = asyncio.run(bybit.Get_Cline_For_all(conf.getValue("exchange", "Coins"), conf.getValue("exchange", "Trade", "Max count of candles for average a trade volume")))

        for i in range (len(self.coins)):
            if (int(result[i]['retCode']) == 0):
                self.coins[result[i]['result']['symbol']].initialize(result[i])
            else:
                failed (result[i])

    def coinSet (self, conf: Config, bybit: Bybit):
        for coin in ((conf.getValue("exchange", "Coins"))):
            self.coins[coin] = Coin(conf, coin, bybit)
