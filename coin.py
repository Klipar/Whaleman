from typing import Dict
from easy import failed, success, inform, warn, test, pr, Config
import asyncio
import aiohttp
from bybit import Bybit
from conditions import CONDITION
from easy.animations import *

from priceStamp import PriceStamp

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
        # ps = PriceStamp(data["data"][0]) # preparing to use PriceStamp

        if (int(data['data'][0]['start']) == int(self.Last_Candle_Start_time)):

            # self.List_of_walues[0][self.limitOfCandles-1] = float(data['data'][0]['open'])
            self.listOfValues[1][0] = float(data['data'][0]['high'])
            self.listOfValues[2][0] = float(data['data'][0]['low'])
            self.listOfValues[3][0] = float(data['data'][0]['close'])
            self.listOfValues[4][0] = float(data['data'][0]['turnover'])
            self.currentCandleTime = int(data['data'][0]['timestamp'])-int(data['data'][0]['start'])
            # pr(self.Curent_Candle_Time)
        elif ((int(data['data'][0]['start']-60000)) == int(self.Last_Candle_Start_time)):
            # warn("NEW CANDLE")
            for i in range (0, 5):
                self.listOfValues[i].pop(0)
            self.listOfValues[0].insert(0, float(data['data'][0]['open']))
            self.listOfValues[1].insert(0, float(data['data'][0]['high']))
            self.listOfValues[2].insert(0, float(data['data'][0]['low']))
            self.listOfValues[3].insert(0, float(data['data'][0]['close']))
            self.listOfValues[4].insert(0, float(data['data'][0]['turnover']))

            self.Last_Candle_Start_time = int(data['data'][0]['start'])
            self.currentCandleTime = int(data['data'][0]['timestamp'])-int(data['data'][0]['start'])
        else:
            coin = [self.coin]
            result = asyncio.run(self.bybit.Get_Cline_For_all(coin, self.limitOfCandles))

            if (int(result[0]['retCode']) == 0):
                self.coins[result[0]['result']['symbol']].Inicialize(result[0])
            else:
                failed (result[0])

            warn ("Data come after one candle, restructing....")
            warn (data['topic'])
        CONDITION(self.config, self.bybit, self)

    def initialize (self, data):
        for i in range (0, self.limitOfCandles):
            self.listOfValues[0][i] = float(data['result']['list'][i][1])
            self.listOfValues[1][i] = float(data['result']['list'][i][2])
            self.listOfValues[2][i] = float(data['result']['list'][i][3])
            self.listOfValues[3][i] = float(data['result']['list'][i][4])
            self.listOfValues[4][i] = float(data['result']['list'][i][6])
        self.Last_Candle_Start_time = int(data['result']['list'][0][0])

    def Get_Last_Prise (self):
        return self.listOfValues[3][0]


class CoinHab:
    def __init__(self, conf: Config, bybit: Bybit):
        self.animation = SimpleAnimation()
        self.coins: Dict[str, Coin] = {}
        self.trashText = 'kline.1.' # зайвий текст що приходить в відповіді від сокета. Він видаляється щоб лишити лише назву монети
        self.coinSet (conf, bybit)
        self.SetRounds(conf, bybit)
        inform (f"Founded {len(self.coins)} Coins")

    def SetRounds(self, conf, bybit: Bybit):
        response = bybit.Get_Instruments_Info()
        for i in response["result"]["list"]:
            for j in ((conf.getValue("exchange", "Coins"))):
                if (i["symbol"] == j):
                    self.coins[j].Set_Round(i)

    def handledr (self, message):
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