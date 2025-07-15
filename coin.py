from easy.massage import failed, success, inform, warn, test, pr
import asyncio
import aiohttp
from conditions import CONDITION
# import json
from easy.animations import *

class Coin:
    def __init__(self, conf, coin, Bybit):
        self.Limit_of_Candels = conf.get_value(parameter1="exchange",parameter2="Treyd", parameter3="Max count of cendals for awereg a treyd wolume")
        self.Coin = coin

        self.Bybit = Bybit
        self.conf = conf

        self.rows = 5    # Кількість типів елементів в масиві
        # Створення двовимірного списку, заповненого нулями
        self.List_of_walues = [[0] * self.Limit_of_Candels for _ in range( self.rows)]
        '''
        self.List_of_walues = [  ['open']
                                 ['high']
                                 ['low']
                                 ['close']
                                 ['turnover']
                              ]
        '''

        self.Last_Candle_Start_time = 0
        self.Curent_Candle_Time = 60000


        self.Prise_Rounf = None
        self.Qty_Step_for_Round = None

    def Get_Curent_order_prise (self):
        return self.Get_Curent_order_prise
    def Get_Coin (self):
        return self.Coin

    def Round_Qty (self, qty):
        return (round(float(qty) / self.Qty_Step_for_Round) * self.Qty_Step_for_Round)
    def Round_Prise (self, prise):
        return round(float(prise), self.Prise_Rounf)

    def Set_Round(self, response):
        # pr (response)
        self.Prise_Rounf = int(response['priceScale'])
        self.Qty_Step_for_Round = float(response['lotSizeFilter']['qtyStep'])

    def Process_Values(self, data):
        if (int(data['data'][0]['start']) == int(self.Last_Candle_Start_time)):

            # self.List_of_walues[0][self.Limit_of_Candels-1] = float(data['data'][0]['open'])
            self.List_of_walues[1][0] = float(data['data'][0]['high'])
            self.List_of_walues[2][0] = float(data['data'][0]['low'])
            self.List_of_walues[3][0] = float(data['data'][0]['close'])
            self.List_of_walues[4][0] = float(data['data'][0]['turnover'])
            self.Curent_Candle_Time = int(data['data'][0]['timestamp'])-int(data['data'][0]['start'])
            # pr(self.Curent_Candle_Time)
        elif ((int(data['data'][0]['start']-60000)) == int(self.Last_Candle_Start_time)):
            # warn("NEW CANDLE")
            for i in range (0, 5):
                self.List_of_walues[i].pop(0)
            self.List_of_walues[0].insert(0, float(data['data'][0]['open']))
            self.List_of_walues[1].insert(0, float(data['data'][0]['high']))
            self.List_of_walues[2].insert(0, float(data['data'][0]['low']))
            self.List_of_walues[3].insert(0, float(data['data'][0]['close']))
            self.List_of_walues[4].insert(0, float(data['data'][0]['turnover']))

            self.Last_Candle_Start_time = int(data['data'][0]['start'])
            self.Curent_Candle_Time = int(data['data'][0]['timestamp'])-int(data['data'][0]['start'])
        else:
            coin = [self.Coin]
            result = asyncio.run(self.Bybit.Get_Cline_For_all(coin, self.Limit_of_Candels))

            if (int(result[0]['retCode']) == 0):
                self.coins[result[0]['result']['symbol']].Inicialize(result[0])
            else:
                failed (result[0])

            warn ("Data come after one candle, restructing....")
            warn (data['topic'])
        CONDITION(self.conf, self.Bybit, self)

    def Inicialize (self, data):
        for i in range (0, self.Limit_of_Candels):
            self.List_of_walues[0][i] = float(data['result']['list'][i][1])
            self.List_of_walues[1][i] = float(data['result']['list'][i][2])
            self.List_of_walues[2][i] = float(data['result']['list'][i][3])
            self.List_of_walues[3][i] = float(data['result']['list'][i][4])
            self.List_of_walues[4][i] = float(data['result']['list'][i][6])
        self.Last_Candle_Start_time = int(data['result']['list'][0][0])

    def Get_Last_Prise (self):
        return self.List_of_walues[3][0]


class CoinHab:
    def __init__(self, conf, Bybit):
        self.animation = SimpleAnimation()
        self.coins = {}              # Створюємо масив об'єктів монет
        self.tresh_text = 'kline.1.' # зайвий текст що приходить в відповіді від сокета. Він видаляється щоб лишити лише назву монети
        self.Coin_Set (conf, Bybit)
        self.SetRounds(conf, Bybit)
        inform (f"Founded {len(self.coins)} Coins")

    def SetRounds(self, conf ,Bybit):
        response = Bybit.Get_Instruments_Info()
        for i in response["result"]["list"]:
            for j in ((conf.get_value(parameter1="exchange",parameter2="Coins"))):
                if (i["symbol"] == j):
                    self.coins[j].Set_Round(i)

        # pr (response)


    def handledr (self, message):
        # if (message['topic'].replace(self.tresh_text, "") == 'ATOMUSDT'):
        inform(self.animation.step(), en="\r")
        self.coins[message['topic'].replace(self.tresh_text, "")].Process_Values(message)
        # test(self.coins[message['topic'].replace(self.tresh_text, "")].Get_Last_Prise())
        # coin = self.coins[message['topic'].replace(self.tresh_text, "")]  # те саме але зручніше для розуміння
        # coin.Process_Values(message)

    def Initialize_Coins (self, conf, Bybit):
        result = asyncio.run(Bybit.Get_Cline_For_all(conf.get_value(parameter1="exchange",parameter2="Coins"), conf.get_value(parameter1="exchange",parameter2="Treyd", parameter3="Max count of cendals for awereg a treyd wolume")))

        for i in range (len(self.coins)):
            if (int(result[i]['retCode']) == 0):
                self.coins[result[i]['result']['symbol']].Inicialize(result[i])
            else:
                failed (result[i])

    def Coin_Set (self, conf, Bybit):
        for i in ((conf.get_value(parameter1="exchange",parameter2="Coins"))):  # створюємо масив монет та заповнюємо його даними з конфігураційного файлу
            obj = Coin(conf, i, Bybit)                                          # Створення об'єкта з переданими значеннями
            self.coins[i] = obj