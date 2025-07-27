from easy.message import *
from easy import Config
from pybit.unified_trading import WebSocket
from pybit.unified_trading import HTTP
from easy.animations import LineProgressBar
import asyncio

from telegramLogger import TelegramLogger


class Bybit:
    def __init__(self, config: Config, telegramLogger: TelegramLogger):
        self.config: Config = config
        self.telegramLogger: TelegramLogger = telegramLogger

        self.webSocket = WebSocket(testnet=self.config.getValue("exchange", "Bybit", "Testnet"),
                                   channel_type=self.config.getValue("exchange", "Bybit", "Category of trading"))

        self.session = HTTP(testnet=config.getValue("exchange", "Bybit", "Testnet"),
                            api_key=config.getValue("exchange", "Bybit", "API Public Key"),
                            api_secret=config.getValue("exchange", "Bybit", "API Secret Key"))

        self.positions = []





        self.Sliding_Persend = float(config.getValue("exchange", "Trade", "Sliding persent from entering prise"))
        self.TakeProfitPersent = float(config.getValue("exchange", "Trade", "Take profit percent from entering prise"))
        self.StopLoss_Persent  = float(config.getValue("exchange", "Trade", "Stop lose percent from entering prise"))
        self.Balance = float(config.getValue("exchange", "Trade", "Max Tradeing Balance in USDT"))
        self.Position_Multiplayer = float(config.getValue("exchange", "Trade", "Multiplier to increase the deal value"))

        self.Next_Persent_step = float(config.getValue("exchange", "Trade", "Next steps prise in percent moowing from last order prise"))

        self.FirstStepPersent = float(config.getValue("exchange", "Trade", "First step in persent from treyding balance"))
        self.MaxOrderPerCoin = int(config.getValue("exchange", "Trade", "Max orders per coin"))



    async def requestForPlacingOrder (self, coin, side: str):
        if (side == "Buy" and self.config.getValue("exchange", "Trade", "Only Sell") or
            side == "Sell" and self.config.getValue("exchange", "Trade", "Only Buy") or
            self.config.getValue("exchange", "Trade", "No Trade")):
            return

        if (self.positions):
            for i in self.positions:
                if (i['symbol'] == coin.coin):
                    move = abs(float(coin.getLastPrise()) - float(i['avgPrice'])) # Реальний здвиг ціни
                    M_move = ((float(i['avgPrice'])/100)*self.Next_Persent_step)    # Максимальний здвиг ціни
                    if (move >= M_move):
                        positionValueNoLeverage = float(i['positionValue'])/float(i['leverage'])
                        expectedPositionValue = positionValueNoLeverage+(positionValueNoLeverage*self.Position_Multiplayer)
                        if (expectedPositionValue <= self.getMaxPositionValue()):
                            if (self.MaxOrderPerCoin > 1):
                                # warn (f"All Goood to plase order another time for {side}")
                                # PREPEARING TO PLASE ORDER
                                symbol = coin.coin
                                qty = coin.roundQty((positionValueNoLeverage*self.Position_Multiplayer))
                                if (side == "Buy"):
                                    prise      = coin.roundPrise(coin.getLastPrise() + ((coin.getLastPrise()/100)*self.Sliding_Persend))
                                    takeProfit = coin.roundPrise(coin.getLastPrise() + ((coin.getLastPrise()/100)*self.TakeProfitPersent))
                                    stopLoss   = coin.roundPrise(coin.getLastPrise() - ((coin.getLastPrise()/100)*self.StopLoss_Persent))
                                else:
                                    prise = coin.roundPrise(coin.getLastPrise() - ((coin.getLastPrise()/100)*self.Sliding_Persend))
                                    takeProfit = coin.roundPrise(coin.getLastPrise() - ((coin.getLastPrise()/100)*self.TakeProfitPersent))
                                    stopLoss   = coin.roundPrise(coin.getLastPrise() + ((coin.getLastPrise()/100)*self.StopLoss_Persent))
                                # Plasing ORDERRRRR
                                    # success("=======================================================")
                                    # test (f"symbol = {symbol}, qty = {qty}, prise = {prise}, side = {side}, takeProfit = {takeProfit}, stopLoss = {stopLoss}")
                                    # success("=======================================================")
                                    await self.placeOrder(symbol = symbol, qty = qty, prise = prise, side = side, takeProfit = takeProfit, stopLoss = stopLoss)
                        else:
                            return
                    failed ("Failed to plase order. limit are accesed")
                    # pr(self.Positions)
                    return

        # warn (f"All Goood to plase order for {side}")
        # PREPEARING TO PLASE ORDER
        symbol = coin.coin

        qty = coin.roundQty((((self.Balance/100)*self.FirstStepPersent)/coin.getLastPrise())*self.config.getValue("exchange", "Trade", "leverage"))
        if (side == "Buy"):
            prise      = coin.roundPrise(coin.getLastPrise() + ((coin.getLastPrise()/100)*self.Sliding_Persend))
            takeProfit = coin.roundPrise(coin.getLastPrise() + ((coin.getLastPrise()/100)*self.TakeProfitPersent))
            stopLoss   = coin.roundPrise(coin.getLastPrise() - ((coin.getLastPrise()/100)*self.StopLoss_Persent))
        else:
            prise = coin.roundPrise(coin.getLastPrise() - ((coin.getLastPrise()/100)*self.Sliding_Persend))
            takeProfit = coin.roundPrise(coin.getLastPrise() - ((coin.getLastPrise()/100)*self.TakeProfitPersent))
            stopLoss   = coin.roundPrise(coin.getLastPrise() + ((coin.getLastPrise()/100)*self.StopLoss_Persent))

        success("=======================================================")
        test (f"symbol = {symbol}, qty = {qty}, prise = {prise}, side = {side}, takeProfit = {takeProfit}, stopLoss = {stopLoss}")
        success("=======================================================")
        await self.placeOrder(symbol = symbol, qty = qty, prise = prise, side = side, takeProfit = takeProfit, stopLoss = stopLoss)

    async def placeOrder(self, symbol, qty, prise, side, takeProfit, stopLoss, orderType = "Limit"):
        try:
            success(self.session.place_order(
                    category=self.config.getValue("exchange", "Bybit", "Category of trading"),
                    symbol=symbol,
                    side=side,
                    orderType=orderType,
                    qty=qty,
                    price=prise,
                    takeProfit=takeProfit,
                    stopLoss=stopLoss))

            await self.telegramLogger.sendPlacingOrder(side=side,
                                                       prise=prise,
                                                       takeProfit=takeProfit,
                                                       stopLoss=stopLoss,
                                                       symbol=symbol,
                                                       qty=qty,
                                                       leverage=self.config.getValue("exchange", "Trade", "leverage"))

        except Exception as e:
            failed(f"Failed to place order: {e}")

    async def getKline(self, symbol):
        return self.session.get_kline(category=self.config.getValue("exchange", "Bybit", "Category of trading"),
                                      symbol=symbol,
                                      interval=self.config.getValue("exchange", "Trade", "Candle time"),
                                      limit=self.config.getValue("exchange", "Trade", "Max count of candles for average a trade volume"))

    async def getClineForAll(self):
        tasks = []
        for symbol in self.config.getValue("exchange", "Coins"):
            tasks.append(asyncio.create_task(self.getKline(symbol)))

        return await asyncio.gather(*tasks)

    async def subscribe(self, coinHab):
        inform ("Subscribing...")

        bar = LineProgressBar(MaxLength = 50, text = "Loading ", maxValue = len(self.config.getValue("exchange", "Coins")), isShowPercent = True, isShowValue = True)
        tasks = []

        async def subscribeCoin(self, coinHab, coin: str, bar: LineProgressBar):
            self.webSocket.kline_stream(interval=self.config.getValue("exchange", "Trade", "Candle time"),
                                 symbol=coin,
                                 callback=coinHab.handler)

            bar.shoveAndUpdate(1)

        for coin in self.config.getValue("exchange", "Coins"):
            tasks.append(subscribeCoin(self=self,coinHab=coinHab, coin=coin, bar=bar))

        await asyncio.gather(*tasks)

    async def refreshPositions(self):
        response = self.session.get_positions(category=self.config.getValue("exchange", "Bybit", "Category of trading"),
                                              settleCoin=self.config.getValue("exchange", "Bybit", "SettleCoin"))

        openOrders = []
        for resp in response['result']['list']:
            if (int(response['time']) >= int(resp['updatedTime'])+60000*self.config.getValue("exchange", "Trade", "Candle time")*self.config.getValue("exchange", "Trade", "Max Count of candle before force closing order") or
                float(resp['unrealisedPnl']) >= self.config.getValue("exchange", "Trade", "Min acceptable profit for pre force closing") and
                int(response['time']) >= int(resp['updatedTime'])+60000*self.config.getValue("exchange", "Trade", "Candle time")*self.config.getValue("Max Count of candle before allowed to close order on acceptable profit")):

                try:
                    side = "Sell" if resp["side"] == "Buy" else "Buy"
                    self.session.place_order(category=response["result"]["category"],
                                             symbol=resp['symbol'],
                                             orderType="Market",
                                             side=side,
                                             qty=resp['size'],
                                             reduce_only=True,
                                             close_on_trigger=False)

                    await self.telegramLogger.sendToAll(f"Closed order on coin: {resp['symbol']}") # TODO: Add another request to telegram bot for closing orders
                    warn (f"Canceled order on {resp['symbol']}")

                except Exception as e:
                    failed(f"Failed to close order on symbol {resp['symbol']}:\n{e}")

            else:
                openOrders.append(resp)

        if int(response["retCode"]) == 0:
            self.positions = openOrders


    def getMaxPositionValue(self):
        maxPositionPercent = self.config.getValue("exchange", "Trade", "Max position percent from balance")
        return (self.Balance/100)*maxPositionPercent

    def getInstrumentsInfo(self):
        return self.session.get_instruments_info(category=self.config.getValue("exchange", "Bybit", "Category of trading"))
