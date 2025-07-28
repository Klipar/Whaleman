from easy.message import *
from easy import Config
from tradingBot.coins.coin import Coin
from tradingBot.model.queueManager import QueueManager

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

async def checkingRateOfPriceChange(coin: Coin):
    thresholdPercentages = coin.config.getValue("exchange", "Trade", "candles minimal move percents")
    stampsList = coin.pricesQueueManager.getStampsList()
    latestStamp = coin.pricesQueueManager.getLatest()

    for i in range (0, len(thresholdPercentages)):
        different = percentMove(stampsList[-(i+1)].open, latestStamp.close) # TODO: In future can be changed to calculate not from "open" candle prise but from avg or something like that

        if different > thresholdPercentages[i]:
            await coin.bybit.requestForPlacingOrder(coin, "Sell")

        elif -different > thresholdPercentages[i]:
            await coin.bybit.requestForPlacingOrder(coin, "Buy")

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

async def checkOrderConditions(coin: Coin):
    if checkingTurnover(config=coin.config, pricesQueueManager=coin.pricesQueueManager): return 0 # Check for sufficient trading volumes

    await checkingRateOfPriceChange(coin)
