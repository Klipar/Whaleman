from easy.message import failed, success, inform, warn, test, pr
from easy import Config
from bybit import Bybit
from coin import Coin

def Checking_turnover (conf: Config, bybit: Bybit, data, coin: Coin):     # перевірка на наявність достатньо високих обємів торгів. Потім додати коофіцієнт часу.
    average = float(calculate_average(data))
    if (conf.getValue("exchange", "Trade", "time factor for trading turnover") == "linear"):
        average = (average*(coin.Curent_Candle_Time/(bybit.Candel_time*60000)))
    if (((float(data[0])/average)*100) > float(conf.getValue("exchange", "Trade", "Triger turnover persent"))):
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


def calculate_average(data):
        total = 0
        for i in data:
            total += float(i)
        return (float(total) / len(data))
def persent_mowe(a, b):
    # a --> b
    # якщо + то ціна піднялася, - то упала
    if a == 0:
        failed("A cant be zero.")
        exit()
    return ((b - a) / a) * 100

def CONDITION (conf, Bybit, coin):
    if(Checking_turnover (conf, Bybit, coin.List_of_walues[4], coin)): return 0 # перевірка достатніх обємів торгів
    Checking_the_rate_of_price_change (conf, Bybit, coin)

    return 0
