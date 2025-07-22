from easy.message import failed, success, inform, warn, test, pr

def Checking_turnover (conf, Bybit, data, coin):     # перевірка на наявність достатньо високих обємів торгів. Потім додати коофіцієнт часу.
    average = float(calculate_average(data))
    if (conf.getValue("exchange", "Treyd", "time factor for trading turnover") == "linear"):
        average = (average*(coin.Curent_Candle_Time/(Bybit.Candel_time*60000)))
    if (((float(data[0])/average)*100) > float(conf.getValue("exchange", "Treyd", "Triger turnover persent"))):
        return 0
    return 1


def Checking_the_rate_of_price_change(conf, Bybit, coin):
    List_of_TRIGER_persents = (conf.getValue("exchange", "Treyd", "cendel minimal move persents"))

    for i in range (0, len(List_of_TRIGER_persents)):
        dif = persent_mowe(float(coin.List_of_walues[0][i+1]), float(coin.List_of_walues[3][0]))
        if (dif > 0):
            if (dif > float(List_of_TRIGER_persents[i])):
                test (f"{dif} ?? {float(List_of_TRIGER_persents[i])}")
                if (My_Bool(conf.getValue("exchange", "Treyd", "Only Buy"))):
                    warn(f"Only Buy, coin si  === > {coin.Get_Coin()}")
                    return
                success ("TRY Sell")
                Bybit.Try_Plase_Order(coin, "Sell")
        else:
            if (dif*(-1) > float(List_of_TRIGER_persents[i])):
                test (f"{dif} ?? {float(List_of_TRIGER_persents[i])}")
                if (My_Bool(conf.getValue("exchange", "Treyd", "Only Sell"))):
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
def My_Bool (test):
    if (test == "True"):
        return True
    return False

def CONDITION (conf, Bybit, coin):
    if(Checking_turnover (conf, Bybit, coin.List_of_walues[4], coin)): return 0 # перевірка достатніх обємів торгів
    Checking_the_rate_of_price_change (conf, Bybit, coin)

    return 0
