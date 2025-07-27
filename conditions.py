from easy.message import *
from easy import Config
from bybit import Bybit
from coin import Coin
from queueManager import QueueManager

def checkingTurnover(config: Config, pricesQueueManager: QueueManager):
    averageTurnover = pricesQueueManager.getAverage("turnover")
    lastStamp = pricesQueueManager.getLatest()

    if (config.getValue("exchange", "Trade", "time factor for trading turnover") == "linear"):
        interval = lastStamp.interval
        executedTimeOfLastCandle = lastStamp.close-lastStamp.timestamp

        averageTurnover = averageTurnover*(executedTimeOfLastCandle/(interval*60000))

    if (lastStamp.turnover/averageTurnover)*100 > config.getValue("exchange", "Trade", "Trigger turnover percent"):
        return 0

    return 1

def Checking_the_rate_of_price_change(config: Config, bybit: Bybit, coin: Coin):
    thresholdPercentages = config.getValue("exchange", "Trade", "candles minimal move percents")
    stampsList = coin.pricesQueueManager.getStampsList()
    latestStamp = coin.pricesQueueManager.getLatest()

    for i in range (0, len(thresholdPercentages)):
        different = percentMove(stampsList[-(i+1)].open, latestStamp.close) # TODO: In future can be changed to calculate not from "open" candle prise but from avg or something like that

        if different > thresholdPercentages[i]:
            if config.getValue("exchange", "Trade", "Only Buy"):
                warn(f"Only Buy, order blocked for {coin.Get_Coin()}")
                return

            success ("TRY Sell")
            bybit.requestForPlacingOrder(coin, "Sell")

        elif -different > thresholdPercentages[i]:
            if config.getValue("exchange", "Trade", "Only Sell"):
                warn(f"Only Sell, order blocked for {coin.Get_Coin()}")
                return

            success ("TRY BUY")
            bybit.requestForPlacingOrder(coin, "Buy")


def percentMove(a: float, b: float) -> float:
    """
    Calculate the percentage change from value 'a' to value 'b'.

    Parameters:
    a (float): The previous value.
    b (float): The current value.

    Returns:
    float: The percentage change from 'a' to 'b'.

    Raises:
    ValueError: If 'a' is zero to prevent division by zero.
    """
    if a == 0:
        raise ValueError("\"A\" cant be zero!")

    return ((b - a) / a) * 100

def shackOrderConditions (config: Config, bybit: Bybit, coin: Coin):
    if checkingTurnover (config=config, pricesQueueManager=coin.pricesQueueManager): return 0 # Check for sufficient trading volumes

    Checking_the_rate_of_price_change (config, bybit, coin)
