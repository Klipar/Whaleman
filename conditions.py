from easy.message import *
from easy import Config
from bybit import Bybit
from coin import Coin
from queueManager import QueueManager

def checkingTurnover(config: Config, pricesQueueManager: QueueManager):     # перевірка на наявність достатньо високих обємів торгів. Потім додати коофіцієнт часу.
    averageTurnover = pricesQueueManager.getAverage("turnover")
    lastStamp = pricesQueueManager.getLatest()

    if (config.getValue("exchange", "Trade", "time factor for trading turnover") == "linear"):
        interval = lastStamp.interval
        executedTimeOfLastCandle = lastStamp.close-lastStamp.timestamp

        averageTurnover = averageTurnover*(executedTimeOfLastCandle/(interval*60000))

    if (lastStamp.turnover/averageTurnover)*100 > config.getValue("exchange", "Trade", "Trigger turnover percent"):
        return 0

    return 1


def Checking_the_rate_of_price_change(conf, Bybit, coin):
    List_of_TRIGER_persents = (conf.getValue("exchange", "Trade", "cendel minimal move persents"))

    for i in range (0, len(List_of_TRIGER_persents)):
        dif = persent_mowe(float(coin.List_of_walues[0][i+1]), float(coin.List_of_walues[3][0]))
        if (dif > 0):
            if (dif > float(List_of_TRIGER_persents[i])):
                test (f"{dif} ?? {float(List_of_TRIGER_persents[i])}")
                if conf.getValue("exchange", "Trade", "Only Buy"):
                    warn(f"Only Buy, coin si  === > {coin.Get_Coin()}")
                    return
                success ("TRY Sell")
                Bybit.Try_Plase_Order(coin, "Sell")
        else:
            if (dif*(-1) > float(List_of_TRIGER_persents[i])):
                test (f"{dif} ?? {float(List_of_TRIGER_persents[i])}")
                if conf.getValue("exchange", "Trade", "Only Sell"):
                    warn(f"Only Sell, coin si  === > {coin.Get_Coin()}")
                    return
                success ("TRY BUY")
                Bybit.Try_Plase_Order(coin, "Buy")


def persent_mowe(a, b):
    # a --> b
    # якщо + то ціна піднялася, - то упала
    if a == 0:
        failed("A cant be zero.")
        exit()
    return ((b - a) / a) * 100

def CONDITION (config: Config, bybit: Bybit, coin: Coin):
    if checkingTurnover (config=config,pricesQueueManager=coin.pricesQueueManager): return 0 # Check for sufficient trading volumes

    Checking_the_rate_of_price_change (config, bybit, coin)

    return 0
