from easy.message import *
from easy import Config
from pybit.unified_trading import WebSocket
from pybit.unified_trading import HTTP
from easy.animations import LineProgressBar, SimpleAnimation
import aiohttp
import asyncio

class Bybit:
    def __init__(self, config: Config):
        self.No_Tradee = config.getValue("exchange", "Trade", "No Trade")
        self.Category  = config.getValue("exchange", "Bybit", "Categoria of treyding")
        self.Candel_time = config.getValue("exchange", "Trade", "Candle time")
        self.SettleCoin = config.getValue("exchange", "Bybit", "SettleCoin")
        self.ws = None
        self.session = HTTP(
            testnet=config.getValue("exchange", "Bybit", "Testnet"),
            api_key=config.getValue("exchange", "Bybit", "API Public Key"),
            api_secret=config.getValue("exchange", "Bybit", "API Secret Key"),
        )
        self.Positions = self.Refresh_Positions ()
        self.Sliding_Persend = float(config.getValue("exchange", "Trade", "Sliding persent from entering prise"))
        self.TakeProfitPersent = float(config.getValue("exchange", "Trade", "Take profit percent from entering prise"))
        self.StopLoss_Persent  = float(config.getValue("exchange", "Trade", "Stop lose percent from entering prise"))
        self.Balanse = float(config.getValue("exchange", "Trade", "Max Tradeing Balance in USDT"))
        self.Position_Multiplayer = float(config.getValue("exchange", "Trade", "Multiplier to increase the deal value"))
        self.Max_Position_Value = float(self.Get_Max_Position_Value(config))
        self.Next_Persent_step = float(config.getValue("exchange", "Trade", "Next steps prise in percent moowing from last order prise"))

        self.FirstStepPersent = float(config.getValue("exchange", "Trade", "First step in persent from treyding balance"))
        self.leverage = float(config.getValue("exchange", "Trade", "leverage"))
        self.MaxOrderPerCoin = int(config.getValue("exchange", "Trade", "Max orders per coin"))

    def requestForPlacingOrder (self, coin, side):
        if (self.Positions):
            for i in self.Positions:
                if (i['symbol'] == coin.Get_Coin()):
                    move = abs(float(coin.Get_Last_Prise()) - float(i['avgPrice'])) # Реальний здвиг ціни
                    M_move = ((float(i['avgPrice'])/100)*self.Next_Persent_step)    # Максимальний здвиг ціни
                    if (move >= M_move):
                        PositionValue_No_Laverage = float(i['positionValue'])/float(i['leverage'])
                        Expectid_Position_value = PositionValue_No_Laverage+(PositionValue_No_Laverage*self.Position_Multiplayer)
                        if (Expectid_Position_value <= self.Max_Position_Value):
                            if (self.MaxOrderPerCoin > 1):
                                # warn (f"All Goood to plase order another time for {side}")
                                # PREPEARING TO PLASE ORDER
                                symbol = coin.Get_Coin()
                                qty = coin.Round_Qty((PositionValue_No_Laverage*self.Position_Multiplayer))
                                if (side == "Buy"):
                                    prise      = coin.Round_Prise(coin.Get_Last_Prise() + ((coin.Get_Last_Prise()/100)*self.Sliding_Persend))
                                    takeProfit = coin.Round_Prise(coin.Get_Last_Prise() + ((coin.Get_Last_Prise()/100)*self.TakeProfitPersent))
                                    stopLoss   = coin.Round_Prise(coin.Get_Last_Prise() - ((coin.Get_Last_Prise()/100)*self.StopLoss_Persent))
                                else:
                                    prise = coin.Round_Prise(coin.Get_Last_Prise() - ((coin.Get_Last_Prise()/100)*self.Sliding_Persend))
                                    takeProfit = coin.Round_Prise(coin.Get_Last_Prise() - ((coin.Get_Last_Prise()/100)*self.TakeProfitPersent))
                                    stopLoss   = coin.Round_Prise(coin.Get_Last_Prise() + ((coin.Get_Last_Prise()/100)*self.StopLoss_Persent))
                                # Plasing ORDERRRRR
                                    # success("=======================================================")
                                    # test (f"symbol = {symbol}, qty = {qty}, prise = {prise}, side = {side}, takeProfit = {takeProfit}, stopLoss = {stopLoss}")
                                    # success("=======================================================")
                                    self.PlaseOrder(symbol = symbol, qty = qty, prise = prise, side = side, takeProfit = takeProfit, stopLoss = stopLoss)
                        else:
                            return
                    failed ("Failed to plase order. limit are accesed")
                    # pr(self.Positions)
                    return

        # warn (f"All Goood to plase order for {side}")
        # PREPEARING TO PLASE ORDER
        symbol = coin.Get_Coin()

        qty = coin.Round_Qty((((self.Balanse/100)*self.FirstStepPersent)/coin.Get_Last_Prise())*self.leverage)
        if (side == "Buy"):
            prise      = coin.Round_Prise(coin.Get_Last_Prise() + ((coin.Get_Last_Prise()/100)*self.Sliding_Persend))
            takeProfit = coin.Round_Prise(coin.Get_Last_Prise() + ((coin.Get_Last_Prise()/100)*self.TakeProfitPersent))
            stopLoss   = coin.Round_Prise(coin.Get_Last_Prise() - ((coin.Get_Last_Prise()/100)*self.StopLoss_Persent))
        else:
            prise = coin.Round_Prise(coin.Get_Last_Prise() - ((coin.Get_Last_Prise()/100)*self.Sliding_Persend))
            takeProfit = coin.Round_Prise(coin.Get_Last_Prise() - ((coin.Get_Last_Prise()/100)*self.TakeProfitPersent))
            stopLoss   = coin.Round_Prise(coin.Get_Last_Prise() + ((coin.Get_Last_Prise()/100)*self.StopLoss_Persent))
        # Plasing ORDERRRRR
        success("=======================================================")
        test (f"symbol = {symbol}, qty = {qty}, prise = {prise}, side = {side}, takeProfit = {takeProfit}, stopLoss = {stopLoss}")
        success("=======================================================")
        self.PlaseOrder(symbol = symbol, qty = qty, prise = prise, side = side, takeProfit = takeProfit, stopLoss = stopLoss)


    def PlaseOrder(self, symbol, qty, prise, side, takeProfit, stopLoss, order_tipe = "Limit"):
        warn(f"--> {side} {symbol}")


        if (self.No_Tradee == True):
            failed (f"skped, no trade = {self.No_Tradee}")
            # self.bot.SEND_TG(warn(f"--> {side} {symbol}"))
            return 0
        try:
            success(self.session.place_order(
                category=self.Category,
                symbol=symbol,
                side=side,
                orderType=order_tipe,
                qty=qty,
                price=prise,
                takeProfit=takeProfit,
                stopLoss=stopLoss
            ))
            # TG_LOG(f"--> {side} {symbol}")
            self.Refresh_Positions()
            logOrderTG(side = side, prise = prise, takeProfit = takeProfit, stopLoss = stopLoss, symbol = symbol, qty = qty, leverage = self.leverage)

            # self.bot.SEND_TG(warn(f"--> {side} {symbol}"))
            # pr ("GOOOOD")
        except Exception as e:
            failed(f"Failed to place order: {e}")

    async def get_kline(self, symbol, limitOfCandles, session = None):
        payload = {}
        headers = {}

        url = f"https://api.bybit.com/v5/market/kline?category={self.Category}&symbol={symbol}&interval={self.Candel_time}&limit={limitOfCandles}"

        async with session.get(url, headers=headers, data=payload) as response:
            data = await response.json()
            try:
                if 'retCode' in data:
                    if (data['retCode'] != 0):
                        failed(f"ERROR while geting candels by REST api, Server returned {data['retCode']}.")
                        return
                    elif not data['result']['list']:
                        failed(f"ERROR while geting candels by REST api, Server du not return list of {symbol}.")
                        return
                    else:
                        return data
                else:
                    failed(f"ERROR while geting candels by REST api, coin is {symbol}")
                    return
            except Exception as e:
                failed(f"ERROR while geting candels by REST api: {e}")

    async def Get_Cline_For_all(self, symbols, limitOfCandles):
        # Сесія для повторного використання HTTP-з'єднань
        async with aiohttp.ClientSession() as session:
            tasks = []
            # Перебір символів і створення завдань
            for symbol in symbols:
                task = asyncio.create_task(self.get_kline(symbol, limitOfCandles, session))
                tasks.append(task)

            # Виконання всіх завдань
            results = await asyncio.gather(*tasks)

            return(results)

    def Subscribe (self, conf, coin_hab):
        inform (f"Subskribing....")
        coins = conf.getValue("exchange", "Coins")

        bar = LineProgressBar(MaxLength = 50, text = "Loading ", maxValue = len(coins), isShowPercent = True, isShowValue = True)

        self.ws = WebSocket(
            testnet=False,
            channel_type=self.Category,
        )

        for symbol in coins:
            self.ws.kline_stream(
                interval=self.Candel_time,
                symbol=symbol,
                callback=coin_hab.handler
            )
            bar.ShoveAndUpdate(1)

    def Refresh_Positions (self):
        response = (self.session.get_positions(
            category=self.Category,
            settleCoin=self.SettleCoin,
        ))


        for i in response['result']['list']:
            if (int(response['time']) >= int(i['updatedTime'])+1000*self.Candel_time*self.CountOfCandleBeforeMarketStop*60 and i['unrealisedPnl'] <= 0.05):
                # print (i['updatedTime'])

                t = (self.session.get_kline(
                    category="linear",
                    symbol=i['symbol'],
                    interval=1,
                    limit=1
                ))

                try:
                    (self.session.set_trading_stop(
                        category="linear",
                        symbol=i['symbol'],
                        stopLoss = float(t['result']['list'][0][4]),
                        # take_profit = float(t['result']['list'][0][4])+3,
                        # TrailingStop = 0.1,
                        slTriggerBy="MarkPrice",
                        positionIdx=0
                    ))
                    warn (f"canseled order on {i['symbol']}")
                except Exception as e:
                    print ("e")



        if (int(response["retCode"]) == 0):
            if (len (response['result']['list'])> 0):
                # pr (response['result']['list'])
                self.Positions = response['result']['list']
                return response['result']['list']
            self.Positions = None
            return None

    def Get_Max_Position_Value (self, conf):
        self.Balanse
        Max_Position_Persent = float(conf.getValue("exchange", "Trade", "Max position persent from balance"))
        return ((self.Balanse/100)*Max_Position_Persent)


    def Get_Instruments_Info (self):
        return (self.session.get_instruments_info(category="linear"))