from typing import Dict
from easy import failed, success, inform, warn, test, pr, Config
import asyncio
import aiohttp
from bybit import Bybit
from conditions import CONDITION
from easy.animations import *

from priceStamp import PriceStamp
from queueManager import QueueManager

class Coin:
    def __init__(self, config: Config, coin: str, bybit: Bybit):
        self.limitOfCandles = config.getValue("exchange", "Trade", "Max count of candles for average a trade volume")
        self.coin: str = coin

        self.bybit: Bybit = bybit
        self.config: Config = config

        self.listOfValues = [[0] * self.limitOfCandles for _ in range(5)]

        self.Last_Candle_Start_time = 0
        self.currentCandleTime = 60000

        self.priseRound = None
        self.qtyStepForRound = None

    def getCoin (self):
        return self.coin

    def Round_Qty (self, qty):
        return (round(float(qty) / self.qtyStepForRound) * self.qtyStepForRound)

    def Round_Prise (self, prise):
        return round(float(prise), self.priseRound)

    def Set_Round(self, response):
        self.priseRound = int(response['priceScale'])
        self.qtyStepForRound = float(response['lotSizeFilter']['qtyStep'])

    def Process_Values(self, data):
        data['data'].sort(key=lambda x: x["start"])

        for data in data['data']:
            self.pricesQueueManager.updateQueue(data)

        CONDITION(self.config, self.bybit, self)

    def initialize (self, data):
        self.pricesQueueManager = QueueManager(data)

    def Get_Last_Prise (self):
        return self.listOfValues[3][0]


class CoinHab:
    def __init__(self, conf: Config, bybit: Bybit):
        self.animation = SimpleAnimation()
        self.coins: Dict[str, Coin] = {}
        self.trashText = f"kline.{conf.getValue("exchange", "Trade", "Cendel time")}." # зайвий текст що приходить в відповіді від сокета. Він видаляється щоб лишити лише назву монети
        self.coinSet (conf, bybit)
        self.SetRounds(conf, bybit)
        inform (f"Founded {len(self.coins)} Coins")

    def SetRounds(self, conf, bybit: Bybit):
        response = bybit.Get_Instruments_Info()
        for i in response["result"]["list"]:
            for j in ((conf.getValue("exchange", "Coins"))):
                if (i["symbol"] == j):
                    self.coins[j].Set_Round(i)

    def handler (self, message):
        inform(self.animation.step(), en="\r")
        self.coins[message['topic'].replace(self.trashText, "")].Process_Values(message)


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